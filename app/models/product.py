from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    name: str
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0) 

class ProductInDB(Product):
    id: Optional[str] = Field(default=None, alias="id")

    class Config:
        populate_by_name = True
        validate_by_name = True

def product_handler(product: dict) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "quantity": product["quantity"],
    }
