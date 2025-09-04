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

        system_instruction = (
            "You are an AI Assistant API with two roles:\n"
            "1. Respond to general user queries.\n"
            "2. Respond to application-related queries about our Inventory system.\n\n"
            "📦 Application Info:\n"
            "- This is a simple Inventory Application.\n"
            "- Each product has: name, price, and quantity.\n"
            f"- Current Products: {product_details}\n\n"
            "📝 Demo Instructions:\n"
            "- To add a product, use the 'Add Product' API.\n"
            "- To view all products, use the 'Get All Products' API.\n"
            "- To get details of a specific product, use the 'Get Product by ID' API.\n"
            "- To find the most expensive product, use 'Get Most Expensive Product'.\n"
            "- To calculate total inventory value, use 'Get Inventory Value'.\n\n"
            "⚡ Example Queries You Can Ask Me:\n"
            "- 'What is the total inventory value?'\n"
            "- 'Which product is the most expensive?'\n"
            "- 'Tell me about the products in stock.'\n"
            "- 'What is the weather in Chennai right now?'\n\n"
            "Note: Keep responses short and clear. Do not elaborate too much.\n\n"
            "Here is the user query -> "
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=system_instruction + prompt.prompt
        )

        return {"message": response.candidates[0].content.parts[0].text}
