from mcp.server import MCPServer

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

import os


# ============================================================
# MCP SERVER
# ============================================================

mcp = MCPServer("Google Drive MCP Server")


# ============================================================
# GOOGLE DRIVE PERMISSION
# ============================================================

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly"
]


# ============================================================
# GOOGLE DRIVE CONNECTION
# ============================================================

def get_drive_service():

    creds = None

    # Existing login
    if os.path.exists("token.json"):

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # Login if required
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save login token
        with open("token.json", "w") as token:

            token.write(creds.to_json())

    # Create Drive service
    service = build(
        "drive",
        "v3",
        credentials=creds
    )

    return service


# ============================================================
# HELPER
# ============================================================

def format_file(file):

    return (
        f"Name: {file.get('name', 'N/A')}\n"
        f"ID: {file.get('id', 'N/A')}\n"
        f"Type: {file.get('mimeType', 'N/A')}\n"
        f"Size: {file.get('size', 'N/A')}\n"
        f"Created: {file.get('createdTime', 'N/A')}\n"
        f"Modified: {file.get('modifiedTime', 'N/A')}\n"
        f"Link: {file.get('webViewLink', 'N/A')}"
    )


# ============================================================
# TOOL 1
# LIST FILES
# ============================================================

@mcp.tool()
def list_files(limit: int = 20) -> str:
    """
    List recent files from Google Drive.
    """

    service = get_drive_service()

    response = (
        service.files()
        .list(
            pageSize=min(limit, 100),
            orderBy="modifiedTime desc",
            q="trashed = false",
            fields=(
                "files("
                "id,"
                "name,"
                "mimeType,"
                "size,"
                "createdTime,"
                "modifiedTime,"
                "webViewLink"
                ")"
            )
        )
        .execute()
    )

    files = response.get("files", [])

    if not files:

        return "No files found."

    output = []

    for index, file in enumerate(files, start=1):

        output.append(
            f"[{index}]\n"
            f"{format_file(file)}\n"
            f"--------------------------------"
        )

    return "\n".join(output)


# ============================================================
# TOOL 2
# SEARCH FILES
# ============================================================

@mcp.tool()
def search_files(query: str, limit: int = 20) -> str:
    """
    Search Google Drive files by name.
    """

    service = get_drive_service()

    safe_query = query.replace("'", "\\'")

    drive_query = (
        f"name contains '{safe_query}' "
        f"and trashed = false"
    )

    response = (
        service.files()
        .list(
            pageSize=min(limit, 100),
            q=drive_query,
            orderBy="modifiedTime desc",
            fields=(
                "files("
                "id,"
                "name,"
                "mimeType,"
                "size,"
                "createdTime,"
                "modifiedTime,"
                "webViewLink"
                ")"
            )
        )
        .execute()
    )

    files = response.get("files", [])

    if not files:

        return f"No files found matching '{query}'."

    output = []

    for index, file in enumerate(files, start=1):

        output.append(
            f"[{index}]\n"
            f"{format_file(file)}\n"
            f"--------------------------------"
        )

    return "\n".join(output)


# ============================================================
# TOOL 3
# GET FILE DETAILS
# ============================================================

@mcp.tool()
def get_file(file_id: str) -> str:
    """
    Get details of a Google Drive file.
    """

    service = get_drive_service()

    try:

        file = (
            service.files()
            .get(
                fileId=file_id,
                fields=(
                    "id,"
                    "name,"
                    "mimeType,"
                    "size,"
                    "createdTime,"
                    "modifiedTime,"
                    "webViewLink,"
                    "webContentLink,"
                    "parents,"
                    "description,"
                    "starred,"
                    "trashed"
                )
            )
            .execute()
        )

        return format_file(file)

    except Exception as e:

        return f"Error getting file: {str(e)}"


# ============================================================
# TOOL 4
# LIST FOLDER FILES
# ============================================================

@mcp.tool()
def list_folder_files(
    folder_id: str,
    limit: int = 50
) -> str:
    """
    List files inside a Google Drive folder.
    """

    service = get_drive_service()

    drive_query = (
        f"'{folder_id}' in parents "
        f"and trashed = false"
    )

    response = (
        service.files()
        .list(
            pageSize=min(limit, 100),
            q=drive_query,
            orderBy="name",
            fields=(
                "files("
                "id,"
                "name,"
                "mimeType,"
                "size,"
                "modifiedTime,"
                "webViewLink"
                ")"
            )
        )
        .execute()
    )

    files = response.get("files", [])

    if not files:

        return "No files found inside this folder."

    output = []

    for index, file in enumerate(files, start=1):

        output.append(
            f"[{index}] "
            f"{file.get('name', 'N/A')} | "
            f"{file.get('mimeType', 'N/A')} | "
            f"{file.get('id', 'N/A')}"
        )

    return "\n".join(output)


# ============================================================
# TOOL 5
# RECENT FILES
# ============================================================

@mcp.tool()
def recent_files(limit: int = 10) -> str:
    """
    Get recently modified Google Drive files.
    """

    service = get_drive_service()

    response = (
        service.files()
        .list(
            pageSize=min(limit, 100),
            q="trashed = false",
            orderBy="modifiedTime desc",
            fields=(
                "files("
                "id,"
                "name,"
                "mimeType,"
                "modifiedTime,"
                "webViewLink"
                ")"
            )
        )
        .execute()
    )

    files = response.get("files", [])

    if not files:

        return "No recent files found."

    output = []

    for index, file in enumerate(files, start=1):

        output.append(
            f"[{index}] "
            f"{file.get('name', 'N/A')}\n"
            f"Modified: {file.get('modifiedTime', 'N/A')}\n"
            f"Type: {file.get('mimeType', 'N/A')}\n"
            f"ID: {file.get('id', 'N/A')}\n"
            f"--------------------------------"
        )

    return "\n".join(output)


# ============================================================
# TOOL 6
# DOWNLOAD FILE
# ============================================================

@mcp.tool()
def download_file(
    file_id: str,
    output_directory: str = "downloads"
) -> str:
    """
    Download a regular Google Drive file.
    """

    service = get_drive_service()

    try:

        file = (
            service.files()
            .get(
                fileId=file_id,
                fields="id,name,mimeType,size"
            )
            .execute()
        )

        file_name = file["name"]

        os.makedirs(
            output_directory,
            exist_ok=True
        )

        output_path = os.path.join(
            output_directory,
            file_name
        )

        request = service.files().get_media(
            fileId=file_id
        )

        with open(output_path, "wb") as output:

            downloader = MediaIoBaseDownload(
                output,
                request
            )

            done = False

            while not done:

                status, done = downloader.next_chunk()

        return (
            f"Download successful.\n"
            f"Name: {file_name}\n"
            f"Path: {output_path}\n"
            f"Type: {file.get('mimeType', 'N/A')}"
        )

    except Exception as e:

        return f"Download failed: {str(e)}"


# ============================================================
# START MCP SERVER
# ============================================================

if __name__ == "__main__":

    mcp.run()