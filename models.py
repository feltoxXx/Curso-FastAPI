from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class CustomerBase(SQLModel):
    name: str = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=100)
    email: str = Field(default=None)
    age: int = Field(default=None)

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    class Config:
        from_attributes = True

class Transaction(BaseModel):
    id: int
    amount: int
    description: str | None

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def total_amount(self):
        return sum([transaction.amount for transaction in self.transactions])