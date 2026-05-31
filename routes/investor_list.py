from fastapi import APIRouter, Query
from typing import Optional
from datetime import date

from data_loader import load_data, filter_by_date, get_date_range_str
from models import InvestorListResponse, InvestorListRecord, DateRange

router = APIRouter()


@router.get("/investor-list", response_model=InvestorListResponse)
def investor_list(
    start_date: Optional[date] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[date] = Query(None, description="End date YYYY-MM-DD"),
):
    """
    Returns a list of all investors with their PAN number, total amount
    invested, total units purchased, and how many distinct funds they invested in.
    """
    data = load_data()
    data = filter_by_date(data, start_date, end_date)

    groups = {}
    for r in data:
        key = (r.get("INV_NAME", ""), r.get("PAN", ""))
        if key not in groups:
            groups[key] = {
                "total_amount_invested": 0.0,
                "total_units_purchased": 0.0,
                "transaction_count": 0,
                "funds": set()
            }
        groups[key]["total_amount_invested"] += r["AMOUNT"]
        groups[key]["total_units_purchased"] += r["UNITS"]
        groups[key]["transaction_count"] += 1
        if r.get("SCHEME"):
            groups[key]["funds"].add(r.get("SCHEME"))

    records = []
    for (inv_name, pan), stats in groups.items():
        records.append(
            InvestorListRecord(
                investor_name=inv_name,
                pan=pan,
                total_amount_invested=round(stats["total_amount_invested"], 2),
                total_units_purchased=round(stats["total_units_purchased"], 4),
                funds_invested_in=len(stats["funds"]),
                transaction_count=stats["transaction_count"],
            )
        )

    # Sort by total amount invested descending
    records.sort(key=lambda r: r.total_amount_invested, reverse=True)

    return InvestorListResponse(
        date_range=DateRange(**get_date_range_str(start_date, end_date)),
        total_investors=len(records),
        data=records,
    )
