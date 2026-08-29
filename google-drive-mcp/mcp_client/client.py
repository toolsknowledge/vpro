import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ============================================================
# MCP SERVER CONFIGURATION
# ============================================================

server_params = StdioServerParameters(
    command="python",
    args=["mcp_server/server.py"]
)


# ============================================================
# CALL TOOL
# ============================================================

async def call_tool(
    session,
    tool_name,
    arguments
):

    result = await session.call_tool(
        tool_name,
        arguments=arguments
    )

    print()
    print("==========================================")
    print("RESULT")
    print("==========================================")
    print()

    for content in result.content:

        if hasattr(content, "text"):

            print(content.text)

    print()


# ============================================================
# SHOW TOOLS
# ============================================================

async def show_tools(session):

    tools = await session.list_tools()

    print()
    print("Available MCP Tools")
    print("===================")

    for index, tool in enumerate(
        tools.tools,
        start=1
    ):

        print(
            f"{index}. {tool.name}"
        )

    print()


# ============================================================
# MAIN
# ============================================================

async def main():

    # Connect to MCP Server
    async with stdio_client(
        server_params
    ) as (read, write):

        # Create MCP Client session
        async with ClientSession(
            read,
            write
        ) as session:

            # Initialize
            await session.initialize()

            print()
            print("==========================================")
            print("       GOOGLE DRIVE MCP CLIENT")
            print("==========================================")
            print()

            print(
                "Connected to MCP Server!"
            )

            # Show tools
            await show_tools(session)

            # ==================================================
            # MENU
            # ==================================================

            while True:

                print("------------------------------------------")
                print("MENU")
                print("------------------------------------------")

                print("1. List Files")
                print("2. Search Files")
                print("3. Get File Details")
                print("4. List Folder Files")
                print("5. Recent Files")
                print("6. Download File")
                print("7. Show MCP Tools")
                print("0. Exit")

                print()

                choice = input(
                    "Enter your choice: "
                ).strip()

                # ==================================================
                # EXIT
                # ==================================================

                if choice == "0":

                    print()
                    print("Goodbye!")

                    break

                # ==================================================
                # LIST FILES
                # ==================================================

                elif choice == "1":

                    limit = input(
                        "Number of files [20]: "
                    ).strip()

                    limit = (
                        int(limit)
                        if limit
                        else 20
                    )

                    await call_tool(
                        session,
                        "list_files",
                        {
                            "limit": limit
                        }
                    )

                # ==================================================
                # SEARCH FILES
                # ==================================================

                elif choice == "2":

                    query = input(
                        "Search file name: "
                    ).strip()

                    if not query:

                        print(
                            "Search cannot be empty."
                        )

                        continue

                    await call_tool(
                        session,
                        "search_files",
                        {
                            "query": query,
                            "limit": 20
                        }
                    )

                # ==================================================
                # GET FILE
                # ==================================================

                elif choice == "3":

                    file_id = input(
                        "Enter File ID: "
                    ).strip()

                    if not file_id:

                        print(
                            "File ID cannot be empty."
                        )

                        continue

                    await call_tool(
                        session,
                        "get_file",
                        {
                            "file_id": file_id
                        }
                    )

                # ==================================================
                # FOLDER FILES
                # ==================================================

                elif choice == "4":

                    folder_id = input(
                        "Enter Folder ID: "
                    ).strip()

                    if not folder_id:

                        print(
                            "Folder ID cannot be empty."
                        )

                        continue

                    await call_tool(
                        session,
                        "list_folder_files",
                        {
                            "folder_id": folder_id,
                            "limit": 50
                        }
                    )

                # ==================================================
                # RECENT FILES
                # ==================================================

                elif choice == "5":

                    await call_tool(
                        session,
                        "recent_files",
                        {
                            "limit": 10
                        }
                    )

                # ==================================================
                # DOWNLOAD FILE
                # ==================================================

                elif choice == "6":

                    file_id = input(
                        "Enter File ID: "
                    ).strip()

                    if not file_id:

                        print(
                            "File ID cannot be empty."
                        )

                        continue

                    await call_tool(
                        session,
                        "download_file",
                        {
                            "file_id": file_id
                        }
                    )

                # ==================================================
                # SHOW TOOLS
                # ==================================================

                elif choice == "7":

                    await show_tools(session)

                # ==================================================
                # INVALID OPTION
                # ==================================================

                else:

                    print(
                        "Invalid choice."
                    )


# ============================================================
# START CLIENT
# ============================================================

if __name__ == "__main__":

    asyncio.run(main())