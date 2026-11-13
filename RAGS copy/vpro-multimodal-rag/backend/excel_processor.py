"""Excel extraction: every worksheet separately, every row as ``Header: value | ...``.

Keeping the column name next to each value means the meaning of a number
("Fee: 30000") is never lost when the row is embedded.
"""
from __future__ import annotations

import datetime as dt
from io import BytesIO

from backend.errors import DocumentReadError, NoExtractableTextError
from backend.models import Section


def _fmt(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, (dt.datetime, dt.date)):
        return value.isoformat(sep=" ") if isinstance(value, dt.datetime) else value.isoformat()
    try:  # pandas NaN / NaT
        if value != value:
            return ""
    except Exception:
        pass
    return str(value).strip()


def _headers(raw: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out = []
    for i, h in enumerate(raw, start=1):
        h = h or f"Column {i}"
        if h in seen:
            seen[h] += 1
            h = f"{h} ({seen[h]})"
        else:
            seen[h] = 1
        out.append(h)
    return out


def row_to_text(headers: list[str], values: list[str]) -> str:
    """``Course: Python Full Stack | Duration: 16 weeks | Fee: 30000`` (empty cells skipped)."""
    return " | ".join(f"{h}: {v}" for h, v in zip(headers, values) if v)


def _sheet_sections(sheet_name: str, rows: list[list[str]], filename: str, file_hash: str, method: str,
                    first_row_number: int = 1) -> list[Section]:
    """rows: all rows as strings; the first non-empty row is the header row."""
    out: list[Section] = []
    header_idx = next((i for i, r in enumerate(rows) if any(r)), None)
    if header_idx is None:
        return out
    headers = _headers(rows[header_idx])
    for i in range(header_idx + 1, len(rows)):
        values = (rows[i] + [""] * len(headers))[: len(headers)]
        text = row_to_text(headers, values)
        if text:
            out.append(Section(text=text, source_file=filename, file_hash=file_hash, document_type="xlsx",
                               extraction_method=method, sheet_name=sheet_name,
                               row_number=first_row_number + i))
    return out


def extract_excel(data: bytes, filename: str, file_hash: str) -> list[Section]:
    ext = filename.lower().rsplit(".", 1)[-1]
    sections: list[Section] = []
    sheet_count = 0
    try:
        if ext == "xlsx":
            from openpyxl import load_workbook
            wb = load_workbook(BytesIO(data), read_only=True, data_only=True)
            for ws in wb.worksheets:
                sheet_count += 1
                rows = [[_fmt(c) for c in r] for r in ws.iter_rows(values_only=True)]
                sections += _sheet_sections(ws.title, rows, filename, file_hash, "openpyxl-rows")
            wb.close()
        else:  # legacy .xls
            import pandas as pd
            sheets = pd.read_excel(BytesIO(data), sheet_name=None, header=None, engine="xlrd")
            for name, df in sheets.items():
                sheet_count += 1
                rows = [[_fmt(c) for c in r] for r in df.itertuples(index=False, name=None)]
                sections += _sheet_sections(str(name), rows, filename, file_hash, "pandas-xlrd-rows")
    except Exception as exc:
        raise DocumentReadError(
            f"'{filename}' could not be read as an Excel file (corrupted or password-protected?): {exc}") from exc
    if not sections:
        raise NoExtractableTextError(f"'{filename}' has {sheet_count} worksheet(s) but no data rows below a header row.")
    return sections
