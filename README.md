# Product Inventory AI Agent  

This is a **FastAPI application** that provides basic product inventory APIs, integrated with **Google Gemini AI Agent** to handle both general user queries and application-related queries.  

---

## 🛠 Tech Stack  
- **Python**: 3.13.5  
- **Pip**: 21.5  
- **MongoDB**: 8.0.13  
- **FastAPI**: modern Python web framework  
- **Uvicorn**: ASGI server for running FastAPI  

---

## Setup Instructions  

1. **Clone the repository**  
```
https://github.com/Yuki-2001/product-inventory-ai-agent.git
cd product-inventory-ai-agent
```

2. **Activate the environment**  
```
.\env\Scripts\activate
```

3. **Install dependencies**  
```
pip install -r version.txt
```

4. **Run the application**  
```
uvicorn app.main:app --reload --port 8000
```

---

## Configuration  
edit a .env file in the project root with the following (Dummy Data):
```
DB_URL=mongodb://localhost:27017
DB_NAME=inventory
GEMINI_AI_KEY=your_google_gemini_api_key_here
```
**DB_URL** → MongoDB connection string
**DB_NAME** → your preferred Mongo database name
**GEMINI_AI_KEY** → Google Gemini API key

---

## API Documentation  

Once the server is running, open Swagger UI:

http://localhost:8000/docs

This provides an interactive API explorer for testing all endpoints.

---

## Features

1. **Product Inventory APIs**

- Add product
- Get all products
- Get product by ID
- Get most expensive product
- Calculate total inventory value

2. **AI Agent Integration**

Handles Both general queries (e.g., weather, facts, etc.) And Supports application-related queries (e.g., product info, totals, etc.)
