from fastapi import HTTPException
from app.config.db_config import mongodb
from ..models.product import product_handler
from bson import ObjectId

collection = lambda: mongodb.db["product"]
class ProductRepository:

    @staticmethod
    async def find_all():
        products = []
        async for product in collection().find({}):
            products.append(product_handler(product))
        return products
    
    @staticmethod
    async def save_product(product) -> dict:
        result = await collection().insert_one(product.dict())
        saved_product = product.dict()
        saved_product["id"] = str(result.inserted_id)
        return saved_product
    
    @staticmethod
    async def get_expensive_product() -> dict:
        product = await collection().find_one(sort=[("price", -1)])
        if not product:
            raise HTTPException(status_code=404, detail="No products found")
        product["id"] = str(product["_id"])
        del product["_id"]
        return product
    
    @staticmethod
    async def get_total_value() -> dict:
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "totalValue": {"$sum": {"$multiply": ["$price", "$quantity"]}}
                }
            }
        ]
        result = await collection().aggregate(pipeline).to_list(length=1)
        total_value = result[0]["totalValue"] if result else 0
        return {"total_value": total_value}
    
    @staticmethod
    async def get_probuct_by_name(name: str):
        return await collection().find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
    
    @staticmethod
    async def get_product_by_id(product_id: str):
        product = await collection().find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    
        product["id"] = str(product["_id"])
        del product["_id"]
        return product
        

