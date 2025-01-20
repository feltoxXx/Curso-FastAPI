from datetime import datetime
import zoneinfo

from fastapi import FastAPI
from sqlmodel import select

from models import Transaction, Invoice
from db import SessionDependency, create_db_and_tables
from .routers import customers, transactions, invoices

app = FastAPI(lifespan=create_db_and_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)

country_timezones = {
    "US": "America/New_York",
    "UK": "Europe/London",
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "ES": "Europe/Madrid",
    "FR": "Europe/Paris",
    "PE": "America/Lima",
    "VE": "America/Caracas",
    "CL": "America/Santiago",
    "EC": "America/Guayaquil",
}

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/time/{iso_code}")
async def get_time(iso_code: str):
    if iso_code.upper() not in country_timezones:
        return {"error": "Invalid ISO code"}
    timezone_str = country_timezones.get(iso_code.upper())
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}





