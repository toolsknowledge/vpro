"""Excel extraction: every worksheet separately, every row as "Header: value" text.

A row such as   | Python Full Stack | 16 weeks | 30000 |
under headers   | Course            | Duration | Fee   |
becomes         "Course: Python Full Stack | Duration: 16 weeks | Fee: 30000"

Keeping the column name next to each value means a chunk still makes sense
when it is read on its own, far away from the header row.
"""

from __future__ import annotations

import io
import math
import zipfile
from datetime import date, datetime

import pandas as pd

from backend.document_loader import DocumentLoadError, ExtractedSection


def _format_value(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value):
            return ""
        if value.is_integer():
            return str(int(value))
    if isinstance(value, (datetime, pd.Timestamp)):
        if value.hour == value.minute == value.second == 0:
            return value.strftime("%Y-%m-%d")
        return value.strftime("%Y-%m-%d %H:%M")
    if isinstance(value, date):
        return value.isoformat()
    return str(value).strip()


def _make_headers(raw_headers: list[str]) -> list[str]:
    """Fill blank headers and make duplicates unique (Column 3, Fee, Fee (2))."""
    headers, seen = [], {}
    for position, header in enumerate(raw_headers, start=1):
        name = header or f"Column {position}"
        count = seen.get(name, 0) + 1
        seen[name] = count
        headers.append(name if count == 1 else f"{name} ({count})")
    return headers


def _read_workbook(data: bytes, filename: str, extension: str) -> dict[str, pd.DataFrame]:
    engine = "openpyxl" if extension == ".xlsx" else "xlrd"
    try:
        return pd.read_excel(io.BytesIO(data), sheet_name=None, header=None, engine=engine, dtype=object)
    except ImportError as exc:
        raise DocumentLoadError(f"Reading {extension} files needs an extra library: {exc}") from exc
    except (zipfile.BadZipFile, ValueError, KeyError, OSError) as exc:
        hint = " Password-protected workbooks are not supported." if extension == ".xlsx" else ""
        raise DocumentLoadError(f"'{filename}' could not be read as an Excel workbook. It may be corrupted.{hint}") from exc
    except Exception as exc:  # xlrd raises its own error types for corrupt .xls files
        raise DocumentLoadError(f"'{filename}' could not be read as an Excel workbook: {exc}") from exc


def extract_excel(data: bytes, filename: str, file_hash: str, extension: str = ".xlsx"):
    workbook = _read_workbook(data, filename, extension)

    sections: list[ExtractedSection] = []
    warnings: list[str] = []
    sheets_with_data = 0

    for sheet_name, frame in workbook.items():
        frame = frame.dropna(how="all").dropna(axis=1, how="all")
        if frame.empty:
            warnings.append(f"Worksheet '{sheet_name}' is empty and was skipped.")
            continue
        sheets_with_data += 1

        # The first non-empty row is treated as the header row.
        header_index = frame.index[0]
        headers = _make_headers([_format_value(v) for v in frame.loc[header_index].tolist()])
        rows = frame.loc[frame.index != header_index]

        if rows.empty:
            # A sheet with only one row: keep it as plain text rather than losing it.
            text = " | ".join(h for h in headers if h)
            sections.append(_section(text, filename, file_hash, sheet_name, int(header_index) + 1))
            continue

        missing_cells = 0
        for index, row in rows.iterrows():
            parts = []
            for header, value in zip(headers, row.tolist()):
                formatted = _format_value(value)
                if formatted:
                    parts.append(f"{header}: {formatted}")
                else:
                    missing_cells += 1
            if parts:
                # pandas index is 0-based; Excel rows are 1-based.
                sections.append(_section(" | ".join(parts), filename, file_hash, sheet_name, int(index) + 1))
        if missing_cells:
            warnings.append(f"Worksheet '{sheet_name}' has {missing_cells} empty cell(s); they were left out of the row text.")

    if not sections:
        raise DocumentLoadError(f"The workbook '{filename}' contains no data.")

    return sections, warnings, {"worksheets": len(workbook), "worksheets_with_data": sheets_with_data, "rows": len(sections)}


def _section(text: str, filename: str, file_hash: str, sheet_name: str, row_number: int) -> ExtractedSection:
    return ExtractedSection(
        text=text,
        source_file=filename,
        file_hash=file_hash,
        document_type="excel",
        extraction_method="pandas/openpyxl row-to-text",
        sheet_name=str(sheet_name),
        row_number=row_number,
        group_key=f"sheet:{sheet_name}",
    )
