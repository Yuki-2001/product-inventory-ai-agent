from ..repositorys.product_repository import ProductRepository
from fastapi import HTTPException

class ProductService:

    @staticmethod
    async def product_list():
        return await ProductRepository.find_all()
    
    @staticmethod
    async def create_product(product):
        same_product= await ProductRepository.get_probuct_by_name(product.name)
        if same_product:
            raise HTTPException(status_code=400, detail="Product with this name already exists")
        return await ProductRepository.save_product(product)
    
    @staticmethod
    async def get_expensive_product():
        return await ProductRepository.get_expensive_product()
    
    @staticmethod
    async def get_total_value():
        return await ProductRepository.get_total_value()
    
    @staticmethod
    async def get_product_by_id(product_id: str):
        return await ProductRepository.get_product_by_id(product_id)