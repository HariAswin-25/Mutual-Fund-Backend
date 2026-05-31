from fastapi import APIRouter, Query
from typing import Optional
from datetime import date

from data_loader import load_data, filter_by_date, get_date_range_str
from models import InvestorPurchaseSummaryResponse, InvestorFundRecord, DateRange

router = APIRouter()


@router.get("/investor-purchase-summary", response_model=InvestorPurchaseSummaryResponse)
def investor_purchase_summary(
    start_date: Optional[date] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[date] = Query(None, description="End date YYYY-MM-DD"),
):
    """
    Returns purchase summary grouped by investor × mutual fund.
    Shows total amount and total units per investor per fund.
    """
    data = load_data()
    data = filter_by_date(data, start_date, end_date)

    groups = {}
    for r in data:
        key = (
            r.get("INV_NAME", ""),
            r.get("PAN", ""),
            r.get("SCHEME", ""),
            r.get("SCHEME_TYPE", "")
        )
        if key not in groups:
            groups[key] = {
                "total_amount": 0.0,
                "total_units": 0.0,
                "transaction_count": 0
            }
        groups[key]["total_amount"] += r["AMOUNT"]
        groups[key]["total_units"] += r["UNITS"]
        groups[key]["transaction_count"] += 1

    records = []
    for (inv_name, pan, scheme, scheme_type), stats in groups.items():
        records.append(
            InvestorFundRecord(
                investor_name=inv_name,
                pan=pan,
                mutual_fund=scheme,
                scheme_type=scheme_type,
                total_amount=round(stats["total_amount"], 2),
                total_units=round(stats["total_units"], 4),
                transaction_count=stats["transaction_count"],
            )
        )

    return InvestorPurchaseSummaryResponse(
        date_range=DateRange(**get_date_range_str(start_date, end_date)),
        total_records=len(records),
        data=records,
    )
