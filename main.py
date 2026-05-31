from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.investor_purchase import router as investor_purchase_router
from routes.fund_wise import router as fund_wise_router
from routes.investor_list import router as investor_list_router
from routes.fund_summary import router as fund_summary_router

app = FastAPI(
    title="Mutual Fund Transaction Dashboard API",
    description=(
        "API for summarizing mutual fund transaction data across investors and schemes. "
        "All endpoints support optional start_date and end_date query parameters (YYYY-MM-DD)."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Allow all origins so the HTML frontend can call the API locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register API routes ───────────────────────────────────────────────────────
app.include_router(investor_purchase_router, prefix="/api", tags=["Investor Purchase Summary"])
app.include_router(fund_wise_router, prefix="/api", tags=["Fund-wise Summary"])
app.include_router(investor_list_router, prefix="/api", tags=["Investor List"])
app.include_router(fund_summary_router, prefix="/api", tags=["Fund Summary"])


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "message": "Mutual Fund Dashboard API is running",
        "docs": "/docs",
        "endpoints": [
            "/api/investor-purchase-summary",
            "/api/fund-wise-summary",
            "/api/investor-list",
            "/api/fund-summary",
        ],
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
