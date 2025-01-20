from datetime import datetime
import zoneinfo

from fastapi import FastAPI, HTTPException, status
from sqlmodel import select

from models import Customer, CustomerCreate, CustomerUpdate, Transaction, Invoice
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


@app.get("/customers", response_model=list[Customer])
async def get_customers(session: SessionDependency):
    return session.exec(select(Customer)).all()


@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDependency):
    customer = Customer.model_validate(customer_data.model_dump())

    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer  


@app.get("/customers/{id}", response_model=Customer)
async def read_customer(id: int, session: SessionDependency):

    customer = session.get(Customer, id) # Esto retorna el mismo resultado que el siguiente
    # customer = session.exec(select(Customer).where(Customer.id == id)).first()

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        
    return customer


@app.delete("/customers/{id}")
async def delete_customer(id: int, session: SessionDependency):
    customer = session.get(Customer, id)

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    session.delete(customer)
    session.commit()
        
    return {"message": "Customer deleted"}


@app.patch("/customers/{id}", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def update_customer(id: int, customer_data: CustomerUpdate, session: SessionDependency):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    update_data = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(update_data)

    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data


@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data