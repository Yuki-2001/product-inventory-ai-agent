# from openai import OpenAI
from google import genai
import json
from ..config.setup_data import setup_data
from ..repositorys.product_repository import ProductRepository

client = genai.Client(api_key=setup_data.GEMINI_API_KEY)
class AiAgentService:

    @staticmethod
    async def ai_agent(prompt):

        # fetch products
        products = await ProductRepository.find_all()

        # convert products to JSON string (safe for OpenAI)
        product_details = json.dumps(products, default=str)

        system_instruction = "You are an AI Assistent API with two works one is to repond general user query and Other is Our Application related user query. this application is simply about inventory has multiple product with name, prize and quantity. Product details are "+ product_details+ ". You no need to reposne ellobrately. Here is the user query -> "
        
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=system_instruction+prompt.prompt
        )
        
        return {"message": response.candidates[0].content.parts[0].text}