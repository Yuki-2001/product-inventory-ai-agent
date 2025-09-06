from fastapi import HTTPException
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
            "Application Info:\n"
            "- This is a simple Inventory Application.\n"
            "- Each product has: name, price, and quantity.\n"
            f"- Current Products: {product_details}\n\n"
            "Demo Instructions:\n"
            "- To add a product, use the 'Add Product' API.\n"
            "- To view all products, use the 'Get All Products' API.\n"
            "- To get details of a specific product, use the 'Get Product by ID' API.\n"
            "- To find the most expensive product, use 'Get Most Expensive Product'.\n"
            "- To calculate total inventory value, use 'Get Inventory Value'.\n\n"
            "Example Queries You Can Ask Me:\n"
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

    async def ai_agent_v2(prompt):

        system_instruction = """
        You are an AI assistant for an Inventory system.

        Decide if the user query is about "products_inventory_application" or "general".
        - if about Application, read the github -> https://github.com/Yuki-2001/product-inventory-ai-agent.git and for API, read openapi.json bin github
        - If about products, ALWAYS return JSON with query info.
        - If about general, return a simple answer.
        JSON Format:
        {
          "type": "product",
          "filters": [
            {"field": "<_id|name|prize|condition>", "operator": "<=|>=|=|<|>|contains|min|max|all", "value": "<optional>"}
          ]
        }
        Examples:
        - "Which is the most expensive product?" 
          → {"type":"product","filters":[{"field":"prize","operator":"max"}]}
        - "Which is the cheapest product?" 
          → {"type":"product","filters":[{"field":"prize","operator":"min"}]}
        - "Show product with id 123" 
          → {"type":"product","filters":[{"field":"_id","operator":"=","value":"123"}]}
        - "List all products" 
          → {"type":"product","filters":[{"field":"*","operator":"all"}]}
        - "Find products with prize less than 500 and condition 'new'"
          → {"type":"product","filters":[
                {"field":"prize","operator":"<","value":500},
                {"field":"condition","operator":"=","value":"new"}
             ]}
        - "What is the weather in Chennai?" 
          → {"type":"general","answer":"Weather is not part of inventory, but here is info..."}
        "Note: Application link is "https://9w9z4l7d-8000.inc1.devtunnels.ms/". Keep responses short and clear. Do not elaborate too much.\n\n"
        -Here is the user Prompt ->
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=system_instruction + prompt.prompt,
        )

        try:
            intent = json.loads(response.candidates[0].content.parts[0].text)
        except Exception:
            raise HTTPException(status_code=500, detail="AI intent parsing failed")

        if intent.get("type") == "product":
            condition = intent.get("condition", {})
            data = await ProductRepository.dynamic_query(condition)
            return {"message": data}

        elif intent.get("type") == "general":
            return {"message": intent.get("answer", "This is a general query.")}

        else:
            return {"message": "I didn’t understand your request."}
