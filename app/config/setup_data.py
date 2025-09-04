from pydantic_settings import BaseSettings

class SetupData(BaseSettings):
    # Base
    APP_NAME: str = "Microservice Base Name"
    APP_DESCRIPTION: str = "Service Description"
    APP_VERSION: str = "1.0.0"
    DEGUG: bool = False

    # Database
    DB_URI: str
    DB_NAME: str
    DB_MAX_POOL_SIZE: int
    DB_MIN_POOL_SIZE: int

    # swagger
    SHOW_DOCS: bool

    #Gemini AI Key
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"

setup_data = SetupData()
