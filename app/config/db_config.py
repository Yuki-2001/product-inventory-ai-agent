from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.setup_data import setup_data
from contextlib import asynccontextmanager
from bson import ObjectId
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue

class DataBase:
    client: AsyncIOMotorClient = None
    db = None

mongodb= DataBase()
async def connect_db():
    mongodb.client = AsyncIOMotorClient(
        setup_data.DB_URI,
        maxPoolSize=setup_data.DB_MAX_POOL_SIZE,     
        minPoolSize=setup_data.DB_MIN_POOL_SIZE,     
        serverSelectionTimeoutMS=5000,               
    )
    mongodb.db = mongodb.client[setup_data.DB_NAME]

async def close_db():
    if mongodb.client:
        mongodb.client.close()

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    await connect_db()
    print("Mongo DB is Connected")
    yield
    await close_db()
    print("Mongo DB is Disconnected")

# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_pydantic_core_schema__(cls, _source_type, _handler) -> core_schema.CoreSchema:
#         # Validation: accept string, convert to ObjectId
#         return core_schema.no_info_after_validator_function(
#             cls.validate,
#             core_schema.str_schema(),
#         )

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid ObjectId")
#         return ObjectId(v)

#     @classmethod
#     def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler) -> JsonSchemaValue:
#         # Display as string in OpenAPI / JSON schema
#         return {"type": "string"}
