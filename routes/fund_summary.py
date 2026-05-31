from fastapi import APIRouter, Query
from typing import Optional
from datetime import date

from data_loader import load_data, filter_by_date, get_date_range_str
from models import FundSummaryResponse, FundSummaryRecord, DateRange

router = APIRouter()


@router.get("/fund-summary", response_model=FundSummaryResponse)
def fund_summary(
    start_date: Optional[date] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[date] = Query(None, description="End date YYYY-MM-DD"),
):
    """
    Returns per-fund aggregation: total amount, total units, average NAV price,
    number of investors, and number of transactions.
    """
    data = load_data()
    data = filter_by_date(data, start_date, end_date)

    groups = {}
    grand_total_amount = 0.0
    grand_total_units = 0.0

    for r in data:
        key = (r.get("SCHEME", ""), r.get("SCHEME_TYPE", ""))
        if key not in groups:
            groups[key] = {
                "total_amount": 0.0,
                "total_units": 0.0,
                "nav_prices": [],
                "investors": set(),
                "transaction_count": 0
            }
        
        groups[key]["total_amount"] += r["AMOUNT"]
        groups[key]["total_units"] += r["UNITS"]
        groups[key]["nav_prices"].append(r["PURPRICE"])
        groups[key]["transaction_count"] += 1
        if r.get("PAN"):
            groups[key]["investors"].add(r.get("PAN"))

        grand_total_amount += r["AMOUNT"]
        grand_total_units += r["UNITS"]

    records = []
    for (scheme, scheme_type), stats in groups.items():
        avg_nav = sum(stats["nav_prices"]) / len(stats["nav_prices"]) if stats["nav_prices"] else 0.0
        records.append(
            FundSummaryRecord(
                mutual_fund=scheme,
                scheme_type=scheme_type,
                total_amount=round(stats["total_amount"], 2),
                total_units=round(stats["total_units"], 4),
                avg_nav_price=round(avg_nav, 4),
                investor_count=len(stats["investors"]),
                transaction_count=stats["transaction_count"],
            )
        )

    # Sort descending by total amount
    records.sort(key=lambda r: r.total_amount, reverse=True)

    return FundSummaryResponse(
        date_range=DateRange(**get_date_range_str(start_date, end_date)),
        grand_total_amount=round(grand_total_amount, 2),
        grand_total_units=round(grand_total_units, 4),
        total_funds=len(records),
        data=records,
    )
