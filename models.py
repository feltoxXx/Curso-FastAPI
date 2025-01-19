from pydantic import BaseModel

class Customer(BaseModel):
    id: int
    name: str
    description: str | None
    email: str
    age: int

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