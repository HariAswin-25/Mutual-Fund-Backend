from fastapi import APIRouter, Query
from typing import Optional
from datetime import date

from data_loader import load_data, filter_by_date, get_date_range_str
from models import FundWiseSummaryResponse, FundWiseRecord, InvestorBreakdown, DateRange

router = APIRouter()


@router.get("/fund-wise-summary", response_model=FundWiseSummaryResponse)
def fund_wise_summary(
    start_date: Optional[date] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[date] = Query(None, description="End date YYYY-MM-DD"),
):
    """
    Returns each mutual fund with a nested breakdown of investors,
    showing how much each investor contributed in amount and units.
    """
    data = load_data()
    data = filter_by_date(data, start_date, end_date)

    # Structure: { (scheme, scheme_type): { (inv_name, pan): {amount, units, transaction_count} } }
    fund_groups = {}
    for r in data:
        f_key = (r.get("SCHEME", ""), r.get("SCHEME_TYPE", ""))
        inv_key = (r.get("INV_NAME", ""), r.get("PAN", ""))

        if f_key not in fund_groups:
            fund_groups[f_key] = {}

        if inv_key not in fund_groups[f_key]:
            fund_groups[f_key][inv_key] = {
                "amount": 0.0,
                "units": 0.0,
                "transaction_count": 0
            }

        fund_groups[f_key][inv_key]["amount"] += r["AMOUNT"]
        fund_groups[f_key][inv_key]["units"] += r["UNITS"]
        fund_groups[f_key][inv_key]["transaction_count"] += 1

    records = []
    for (scheme, scheme_type), investors_dict in fund_groups.items():
        investors = []
        total_amount = 0.0
        total_units = 0.0

        for (inv_name, pan), stats in investors_dict.items():
            investors.append(
                InvestorBreakdown(
                    investor_name=inv_name,
                    pan=pan,
                    amount=round(stats["amount"], 2),
                    units=round(stats["units"], 4),
                    transaction_count=stats["transaction_count"],
                )
            )
            total_amount += stats["amount"]
            total_units += stats["units"]

        records.append(
            FundWiseRecord(
                mutual_fund=scheme,
                scheme_type=scheme_type,
                investors=investors,
                total_amount=round(total_amount, 2),
                total_units=round(total_units, 4),
                investor_count=len(investors),
            )
        )

    return FundWiseSummaryResponse(
        date_range=DateRange(**get_date_range_str(start_date, end_date)),
        total_funds=len(records),
        data=records,
    )
