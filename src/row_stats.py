# Build: 0364e55c775d5efc1d1e158af145cee8
"""Summarize a numeric column from a CSV file without modifying the input."""

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean, median


def read_numbers(path: Path, column: str) -> list[float]:
    values: list[float] = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if column not in (reader.fieldnames or []):
            raise ValueError(f"Column {column!r} is missing")
        for row_number, row in enumerate(reader, start=2):
            raw = (row.get(column) or "").strip()
            if not raw:
                continue
            try:
                value = float(raw)
                if not math.isfinite(value):
                    raise ValueError("number must be finite")
                values.append(value)
            except ValueError as error:
                raise ValueError(f"Invalid number on row {row_number}: {raw!r}") from error
    return values


def summarize(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None, "median": None}
    return {"count": len(values), "minimum": min(values), "maximum": max(values),
            "mean": mean(values), "median": median(values)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("column")
    args = parser.parse_args()
    print(json.dumps(summarize(read_numbers(args.csv_file, args.column)), indent=2))


if __name__ == "__main__":
    main()
