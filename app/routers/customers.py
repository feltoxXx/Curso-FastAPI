from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from models import Customer, CustomerCreate, CustomerUpdate
from db import SessionDependency



router = APIRouter()

@router.get("/customers", response_model=list[Customer], tags=["customers"])
async def get_customers(session: SessionDependency):
    return session.exec(select(Customer)).all()


@router.post("/customers", response_model=Customer, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDependency):
    customer = Customer.model_validate(customer_data.model_dump())

    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer  


@router.get("/customers/{id}", response_model=Customer, tags=["customers"])
async def read_customer(id: int, session: SessionDependency):

    customer = session.get(Customer, id) # Esto retorna el mismo resultado que el siguiente
    # customer = session.exec(select(Customer).where(Customer.id == id)).first()

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        
    return customer


@router.delete("/customers/{id}", tags=["customers"])
async def delete_customer(id: int, session: SessionDependency):
    customer = session.get(Customer, id)

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    session.delete(customer)
    session.commit()
        
    return {"message": "Customer deleted"}


@router.patch("/customers/{id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["customers"])
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

