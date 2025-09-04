from fastapi import APIRouter
from ..models.ai_agent import PromptModel, ResponseModel
from ..services.ai_agent_service import AiAgentService

router = APIRouter(prefix="/aiagent", tags=["AI Agent"])

@router.post("/prompt", response_model=ResponseModel)
async def ai_agent(prompt: PromptModel):
    return await AiAgentService.ai_agent(prompt)