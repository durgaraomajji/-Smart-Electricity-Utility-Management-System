from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.utils.exceptions import AppException, app_exception_handler

from app.routes import (
    auth, customers, connections, meters, readings, tariffs, bills,
    payments, complaints, technicians, service_requests, analytics,
    dashboard, reports
)

app = FastAPI(
    title="Smart Electricity Utility Management System",
    description="Electricity utility management APIs with OAuth2 Password Flow, JWT, RBAC, billing, payments, complaints and analytics.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Smart Electricity Utility Management System", "docs": "/docs"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(connections.router)
app.include_router(meters.router)
app.include_router(readings.router)
app.include_router(tariffs.router)
app.include_router(bills.router)
app.include_router(payments.router)
app.include_router(complaints.router)
app.include_router(technicians.router)
app.include_router(service_requests.router)
app.include_router(analytics.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
