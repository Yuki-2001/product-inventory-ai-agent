from fastapi import FastAPI
from app.config.setup_data import setup_data
from app.config.db_config import db_lifespan
from .routes import product_routes, ai_agent_router

app = FastAPI(
    title= setup_data.APP_NAME,
    description=setup_data.APP_DESCRIPTION,
    version=setup_data.APP_VERSION,    
    docs_url="/docs" if setup_data.SHOW_DOCS else None,
    lifespan=db_lifespan
    )

ROUTERS = [product_routes.router, ai_agent_router.router]

for router in ROUTERS:
    app.include_router(router, prefix="/api/v1")

@app.get("/")
async def say_hello():
    return {"message":"hello"}