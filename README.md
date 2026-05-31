# WealthSync Backend

Lightweight, high-performance REST API designed to process, aggregate, and filter mutual fund transaction logs. 

Built using **FastAPI** and Python standard libraries—completely **Pandas-free**. It is natively compatible with Python 3.13.13+ out-of-the-box and starts in milliseconds.

## Directory Structure
```
backend/
├── routes/
│   ├── investor_purchase.py  # Endpoint 1: Investor × Scheme Purchase Summary
│   ├── fund_wise.py          # Endpoint 2: Fund-wise Summary per Investor
│   ├── investor_list.py      # Endpoint 3: Investor List & PAN Ledger
│   └── fund_summary.py       # Endpoint 4: Mutual Fund Summaries & NAV averages
├── data_loader.py            # Custom quotes stripping, clean types & date parser
├── models.py                 # Pydantic response models
├── main.py                   # FastAPI app entry point & CORS configuration
├── requirements.txt          # Lightweight pip dependencies
└── dataset.csv               # Mutual fund transaction log dataset
```

## Quick Start

### 1. Install Dependencies
Make sure you have Python 3.8+ installed. Run the following command:
```bash
pip install -r requirements.txt
```

### 2. Start the Server
Run the FastAPI application on **port 8001** with hot-reload enabled:
```bash
uvicorn main:app --port 8001 --reload
```
The server will start on [http://127.0.0.1:8001](http://127.0.0.1:8001).

---

## API Endpoints

All endpoints support optional filtering via query parameters:
* `start_date`: Start filter date (`YYYY-MM-DD`, e.g., `2025-05-27`)
* `end_date`: End filter date (`YYYY-MM-DD`, e.g., `2025-05-27`)

### 1. Investor-wise Purchase Summary per Mutual Fund
* **Route**: `GET /api/investor-purchase-summary`
* **Description**: Returns transactions aggregated by unique combination of Investor + PAN + Mutual Fund.
* **Response Sample**:
```json
{
  "date_range": { "start": "2025-05-27", "end": "2025-05-27" },
  "total_records": 1,
  "data": [
    {
      "investor_name": "Meethala Pullutummal Narayani",
      "pan": "AAEPN3766A",
      "mutual_fund": "DSP Nifty 50 Equal Weight Index Fund - Reg - Growth",
      "scheme_type": "Index Fund",
      "total_amount": 6499.68,
      "total_units": 261.49,
      "transaction_count": 1
    }
  ]
}
```

### 2. Mutual Fund-wise Summary per Investor
* **Route**: `GET /api/fund-wise-summary`
* **Description**: Returns all mutual fund schemes, containing nested arrays of investors who contributed to that scheme. Useful for drill-down accordion elements.
* **Response Sample**:
```json
{
  "date_range": { "start": "2025-05-27", "end": "2025-05-27" },
  "total_funds": 1,
  "data": [
    {
      "mutual_fund": "Kotak Gold Fund - Growth (Regular Plan)",
      "scheme_type": "Gold FOF",
      "investors": [
        {
          "investor_name": "Shilpa J Suresh",
          "pan": "FRSPS3248J",
          "amount": 1491.93,
          "units": 40.43,
          "transaction_count": 1
        }
      ],
      "total_amount": 1491.93,
      "total_units": 40.43,
      "investor_count": 1
    }
  ]
}
```

### 3. Investor List with Purchase Details
* **Route**: `GET /api/investor-list`
* **Description**: Lists all unique investors sorted by total capital invested in descending order. Includes unique PAN, total units, and distinct fund counts.
* **Response Sample**:
```json
{
  "date_range": { "start": "2025-05-27", "end": "2025-05-27" },
  "total_investors": 1,
  "data": [
    {
      "investor_name": "M Padmapriya",
      "pan": "ANIPP0516B",
      "total_amount_invested": 31499.5,
      "total_units_purchased": 117.44,
      "funds_invested_in": 3,
      "transaction_count": 4
    }
  ]
}
```

### 4. Mutual Fund Summary
* **Route**: `GET /api/fund-summary`
* **Description**: Returns macro aggregation stats per scheme including total invested capital, total NAV units, average NAV price, and investor counters. Sorted by total capital in descending order.
* **Response Sample**:
```json
{
  "date_range": { "start": "2025-05-27", "end": "2025-05-27" },
  "grand_total_amount": 31499.5,
  "grand_total_units": 117.44,
  "total_funds": 1,
  "data": [
    {
      "mutual_fund": "SBI Small Cap Fund Regular Growth",
      "scheme_type": "Equity(G)",
      "total_amount": 9999.5,
      "total_units": 59.62,
      "avg_nav_price": 167.71,
      "investor_count": 1,
      "transaction_count": 1
    }
  ]
}
```

---

## Interactive Docs
FastAPI automatically generates documentation. Open your browser and navigate to:
* **Swagger UI**: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
* **ReDoc**: [http://127.0.0.1:8001/redoc](http://127.0.0.1:8001/redoc)
