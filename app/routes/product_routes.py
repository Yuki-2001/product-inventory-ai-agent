from fastapi import APIRouter, HTTPException
from typing import List
from ..services.product_services import ProductService
from ..models.product import ProductInDB, Product
from bson import ObjectId

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductInDB])
async def list_products():
    return await ProductService.product_list()

@router.post("/", response_model=ProductInDB)
async def creat_products(product: Product):
    return await ProductService.create_product(product)

@router.get("/products/expensive", response_model=ProductInDB)
async def get_expensive_product():
    return await ProductService.get_expensive_product()

@router.get("/products/total-value")
async def get_total_value():
    return await ProductService.get_total_value()

@router.get("/products/{product_id}", response_model=ProductInDB)
async def get_product_by_id(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    return await ProductService.get_product_by_id(product_id)
