import csv
import os
from datetime import datetime, date
from typing import List, Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "dataset.csv")

_data_cache: Optional[List[Dict[str, Any]]] = None


def load_data() -> List[Dict[str, Any]]:
    """Load and cache the CSV dataset, cleaning single quotes, spaces, and formatting types."""
    global _data_cache
    if _data_cache is not None:
        return _data_cache

    cleaned_records = []
    
    if not os.path.exists(CSV_PATH):
        return []

    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        # Read the raw lines to handle potential trailing newlines and strip outer quotes
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            return []
            
        headers = [h.strip().strip("'") for h in headers]

        for row in reader:
            if not row:
                continue
            
            # Clean values
            row_vals = [val.strip().strip("'") for val in row]
            
            # Create dict matching cleaned headers to cleaned values
            record = dict(zip(headers, row_vals))
            
            # Parse numbers
            try:
                record["PURPRICE"] = float(record.get("PURPRICE") or 0.0)
            except ValueError:
                record["PURPRICE"] = 0.0

            try:
                record["UNITS"] = float(record.get("UNITS") or 0.0)
            except ValueError:
                record["UNITS"] = 0.0

            try:
                record["AMOUNT"] = float(record.get("AMOUNT") or 0.0)
            except ValueError:
                record["AMOUNT"] = 0.0

            # Parse trade date (Format: '5/27/2025 12:00:00 AM')
            trad_date_str = record.get("TRADDATE", "")
            parsed_dt = None
            if trad_date_str:
                for fmt in ("%m/%d/%Y %I:%M:%S %p", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                    try:
                        parsed_dt = datetime.strptime(trad_date_str, fmt).date()
                        break
                    except ValueError:
                        continue
            record["parsed_date"] = parsed_dt
            
            cleaned_records.append(record)

    _data_cache = cleaned_records
    return cleaned_records


def filter_by_date(
    data: List[Dict[str, Any]],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[Dict[str, Any]]:
    """Return record dicts within the given inclusive date range."""
    filtered = []
    for record in data:
        tx_date = record.get("parsed_date")
        if not tx_date:
            continue
        if start_date and tx_date < start_date:
            continue
        if end_date and tx_date > end_date:
            continue
        filtered.append(record)
    return filtered


def get_date_range_str(start_date: Optional[date], end_date: Optional[date]) -> Dict[str, Optional[str]]:
    return {
        "start": str(start_date) if start_date else None,
        "end": str(end_date) if end_date else None,
    }
