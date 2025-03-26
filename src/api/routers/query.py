from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from src.services.asking_snowflake import VannaAsker
from src.core.vanna import MyVanna
from src.core.sf_handler import connect_to_snowflake
from src.config.local_env import AppConfig
from src.services.vanna_calls import (
    generate_questions_cached,
    generate_sql_cached,
    run_sql_cached,
    generate_plotly_code_cached,
    generate_plot_cached,
    generate_followup_cached,
    should_generate_chart_cached,
    is_sql_valid_cached,
    generate_summary_cached
)
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(prefix="/query", tags=["Query Endpoints"])

def create_asker(index_name: str):
    """Creates a new instance of VannaAsker with a specific index name."""
    config = {
        "azure_search_endpoint": os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
        "azure_search_api_key": os.getenv("AZURE_SEARCH_API_KEY"),
        "index_name": index_name,
        "dimensions": 384,
        "model": os.getenv("MODEL")
    }
    vn_instance = MyVanna(config=config)  
    vn_instance = connect_to_snowflake(vn_instance)  
    return vn_instance

class AskRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(
    request: AskRequest, 
    index_name: str = Query(..., description="Azure AI Search index name"),
):
    asker = create_asker(index_name)
    generated_sql_query = generate_sql_cached(asker, request.question)
    is_sql_query_valid = is_sql_valid_cached(asker, sql=generated_sql_query)
    return_from_sql_query = run_sql_cached(asker, sql=generated_sql_query)
    summary = generate_summary_cached(asker, question=request, df=return_from_sql_query)

    response = {
        "gen_sql_qeury": generated_sql_query,
        "result_from_query": return_from_sql_query.to_dict('records'),
        "summary": summary
    }
    return response

@router.get("/suggested-questions")
def get_suggested_questions(
    index_name: str = Query(..., description="Azure AI Search index name"),
):
    """Fetch suggested questions from Vanna."""
    try:
        asker = create_asker(index_name)
        return generate_questions_cached(asker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
