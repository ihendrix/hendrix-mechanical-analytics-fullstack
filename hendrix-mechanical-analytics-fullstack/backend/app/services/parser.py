from __future__ import annotations

import csv
import io
import re
import zipfile
from pathlib import Path

import pandas as pd

SUPPORTED_FILE_EXTENSIONS = {".csv", ".xlsx", ".xls", ".txt", ".dat", ".tsv"}


def safe_name(filename: str) -> str:
    name = Path(filename).stem
    name = re.sub(r"\s*\(\d+\)$", "", name)
    name = name.replace("_corrected", "")
    name = name.replace("_", " ")
    return re.sub(r"\s+", " ", name).strip()


def _clean_header_value(value, index):
    if pd.isna(value):
        return "Specimen" if index == 0 else f"Column {index + 1}"

    name = str(value).strip()
    if not name or name.lower().startswith("unnamed"):
        return "Specimen" if index == 0 else f"Column {index + 1}"

    return name


def _make_unique_columns(values):
    output = []
    counts = {}

    for i, value in enumerate(values):
        base = _clean_header_value(value, i)
        counts[base] = counts.get(base, 0) + 1
        output.append(base if counts[base] == 1 else f"{base} ({counts[base]})")

    return output


def _find_header_row(raw: pd.DataFrame, max_rows: int = 30):
    terms = [
        "strain",
        "stress",
        "load",
        "extension",
        "displacement",
        "time measurement",
        "specimen",
    ]

    best_index = 0
    best_score = -1

    for index in range(min(max_rows, len(raw))):
        row_text = " | ".join(
            str(value).strip().lower()
            for value in raw.iloc[index].tolist()
            if not pd.isna(value)
        )

        score = sum(term in row_text for term in terms)
        if "strain" in row_text and "stress" in row_text:
            score += 10

        if score > best_score:
            best_index = index
            best_score = score

    return best_index if best_score > 0 else 0


def _promote_detected_header(raw: pd.DataFrame) -> pd.DataFrame:
    raw = raw.dropna(axis=0, how="all").dropna(axis=1, how="all").reset_index(drop=True)

    if raw.empty:
        return raw

    header_index = _find_header_row(raw)
    columns = _make_unique_columns(raw.iloc[header_index].tolist())

    df = raw.iloc[header_index + 1 :].copy().reset_index(drop=True)
    df.columns = columns
    df = df.dropna(axis=0, how="all").dropna(axis=1, how="all")

    return df.reset_index(drop=True)


def _decode_text(data: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def _detect_delimiter(text: str, suffix: str) -> str:
    if suffix == ".csv":
        return ","
    if suffix == ".tsv":
        return "\t"

    lines = [line for line in text.splitlines() if line.strip()][:30]
    candidates = [",", "\t", ";", "|"]
    scores = {delimiter: sum(line.count(delimiter) for line in lines) for delimiter in candidates}
    best = max(scores, key=scores.get)

    return best if scores[best] > 0 else ","


def _read_ragged_delimited(data: bytes, suffix: str) -> pd.DataFrame:
    text = _decode_text(data)
    delimiter = _detect_delimiter(text, suffix)

    rows = []
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    for row in reader:
        if row and any(str(cell).strip() for cell in row):
            rows.append(row)

    if not rows:
        return pd.DataFrame()

    width = max(len(row) for row in rows)
    padded = [row + [None] * (width - len(row)) for row in rows]
    return pd.DataFrame(padded, dtype=object)


def read_file_bytes(filename: str, data: bytes) -> pd.DataFrame:
    suffix = Path(filename).suffix.lower()

    if suffix in [".xlsx", ".xls"]:
        raw = pd.read_excel(io.BytesIO(data), header=None)
    else:
        raw = _read_ragged_delimited(data, suffix)

    return _promote_detected_header(raw)


def iter_uploaded_payloads(files: list[tuple[str, bytes]]):
    for filename, data in files:
        suffix = Path(filename).suffix.lower()

        if suffix != ".zip":
            yield filename, data
            continue

        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue

                member_path = Path(member.filename)
                member_suffix = member_path.suffix.lower()

                if member_suffix not in SUPPORTED_FILE_EXTENSIONS:
                    continue
                if member_path.name.startswith(".") or "__MACOSX" in member.parts:
                    continue

                yield member_path.name, archive.read(member)
