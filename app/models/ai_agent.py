from pydantic import BaseModel, Field
from typing import Optional

class PromptModel(BaseModel):
    prompt: str

class ResponseModel(BaseModel):
    message: str