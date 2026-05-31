from pydantic import BaseModel
from typing import List, Optional


class DateRange(BaseModel):
    start: Optional[str]
    end: Optional[str]


# ── Endpoint 1: Investor-wise Purchase Summary per Fund ──────────────────────

class InvestorFundRecord(BaseModel):
    investor_name: str
    pan: str
    mutual_fund: str
    scheme_type: str
    total_amount: float
    total_units: float
    transaction_count: int


class InvestorPurchaseSummaryResponse(BaseModel):
    date_range: DateRange
    total_records: int
    data: List[InvestorFundRecord]


# ── Endpoint 2: Fund-wise Summary per Investor ───────────────────────────────

class InvestorBreakdown(BaseModel):
    investor_name: str
    pan: str
    amount: float
    units: float
    transaction_count: int


class FundWiseRecord(BaseModel):
    mutual_fund: str
    scheme_type: str
    investors: List[InvestorBreakdown]
    total_amount: float
    total_units: float
    investor_count: int


class FundWiseSummaryResponse(BaseModel):
    date_range: DateRange
    total_funds: int
    data: List[FundWiseRecord]


# ── Endpoint 3: Investor List with Purchase Details ──────────────────────────

class InvestorListRecord(BaseModel):
    investor_name: str
    pan: str
    total_amount_invested: float
    total_units_purchased: float
    funds_invested_in: int
    transaction_count: int


class InvestorListResponse(BaseModel):
    date_range: DateRange
    total_investors: int
    data: List[InvestorListRecord]


# ── Endpoint 4: Mutual Fund Summary ─────────────────────────────────────────

class FundSummaryRecord(BaseModel):
    mutual_fund: str
    scheme_type: str
    total_amount: float
    total_units: float
    avg_nav_price: float
    investor_count: int
    transaction_count: int


class FundSummaryResponse(BaseModel):
    date_range: DateRange
    grand_total_amount: float
    grand_total_units: float
    total_funds: int
    data: List[FundSummaryRecord]
