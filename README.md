# Vanna AI + Azure AI Search Integration

This project integrates Vanna.AI with Azure AI Search as a vector database, replacing the default ChromaDB or other alternatives. Built on FastAPI, it offers endpoints for training and querying SQL-related insights using documents, schemas, and prompt/SQL pairs.

## How it works
![vanna-quadrants](https://github.com/vanna-ai/vanna/assets/7146154/1c7c88ba-c144-4ecf-a028-cf5ba7344ca2)

![Screen Recording 2024-01-24 at 11 21 37 AM](https://github.com/vanna-ai/vanna/assets/7146154/1d2718ad-12a8-4a76-afa2-c61754462f93)

## 🚀 Features 
- ✅ Ask natural language questions and receive SQL queries with results

- 📄 Train on:

    - Information schema (from Snowflake)

    - Business documents

    - Prompt/SQL pairs

    - DDL structures (WIP)

- 🧠 Powered by Azure AI Search with embedding via fastembed


## Structure
```
src/
├── api/
│   ├── main.py              # FastAPI entrypoint
│   ├── schemas.py           # Pydantic request/
|   └── routers
|       ├── training.py
|       └── query.py
|
├── config/
│   └── local_env.py
|
├── core/
|   ├── __init__.py
|   ├── azure_client.py     # Creates client with Azure
|   ├── azure_custom_db.py  # Handler for AI Search DB
|   ├── sf_handler.py       # Snowflake Client
|   ├── vanna.py            # Custom Vanna (snowflake + OpenAI + AzureSearchDB)
|
├── services/
│   ├── __init__.py     
|   ├── asking_snowflake.py 
|   ├── ddl.py 
|   ├── training.py 
|   ├── vanna_calls.py 

```

## Setup

1. Install Dependencies
``` 
pip3 install -r requirments.txt
```

2. Add Enviroment Variables
```
# Azure AI Search
AZURE_AI_SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
AZURE_SEARCH_API_KEY=your-azure-search-api-key
MODEL=gpt-4

# Snowflake Config
SF_USER=your_snowflake_user
SF_PASSWORD=your_snowflake_password
SF_ACCOUNT=your_snowflake_account
SF_WAREHOUSE=your_warehouse
SF_DATABASE=your_database
SF_ROLE=your_role

# Azure OpenAI (for embeddings & chat)
ENDPOINT=https://<your-openai-endpoint>.openai.azure.com
KEY=your-openai-api-key
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

3. Run the API
```
uvicorn src.api.main:app --reload
```

## API Endpoints

## 📖 API Endpoints

### 🧠 Training Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/training/train_base_data?index_name=...` | Trains on Snowflake info schema, business rules, and prompt/SQL pairs |
| POST   | `/training/train_documents?index_name=...` | Trains on plain text documentation |
| POST   | `/training/train_prompt_sql_pairs?index_name=...` | Trains on (question, SQL) pairs |
| POST   | `/training/train_ddl?index_name=...` | Trains on DDL (currently not implemented) |
| GET    | `/training/get_training_data?index_name=...` | Returns current training data stored in Azure AI Search |

### ❓ Query Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/query/ask?index_name=...` | Submits a question, returns SQL, result, and summary |
| GET    | `/query/suggested-questions?index_name=...` | Fetches AI-generated sample questions for the dataset |



## 📈 Azure AI Vector Search

The custom vector store (AzureAISearch_VectorStore) provides embedding and semantic search capabilities via:

- add_documentation()

- add_question_sql()

- get_related_documentation()

- get_similar_question_sql()

- See implementation in: src/core/azure_vectorstore.py


## Credits

- VannaAI - https://vanna.ai/
- Azure AI Search - https://learn.microsoft.com/en-us/azure/search/
- FastAPI - https://fastapi.tiangolo.com/


