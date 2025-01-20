from datetime import datetime
import zoneinfo

from fastapi import FastAPI
from sqlmodel import select

from models import Customer, CustomerCreate, Transaction, Invoice
from db import SessionDependency, create_db_and_tables

app = FastAPI(lifespan=create_db_and_tables)

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



@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDependency):
    customer = Customer.model_validate(customer_data.model_dump())

    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer


@app.get("/customers", response_model=list[Customer])
async def list_customer(session: SessionDependency):
    return session.exec(select(Customer)).all()
    


@app.get("/customer/{id}")
async def get_customer(id: int, session: SessionDependency):
    customer = session.exec(select(Customer).where(Customer.id == id)).first()
    if not customer:
        return {"error": "Customer not found"}
        
    return customer
    


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data


@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data