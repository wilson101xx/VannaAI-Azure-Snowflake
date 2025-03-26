import json
import os
from fastapi import APIRouter, HTTPException, Depends, Query
from dotenv import load_dotenv
from src.core.vanna import MyVanna
from src.core.sf_handler import connect_to_snowflake
from src.services.training import VannaTrainer
from src.api import schemas

load_dotenv()

router = APIRouter(prefix="/training", tags=["Training Endpoints"])

def create_trainer(index_name: str) -> VannaTrainer:
    config = {
        "azure_search_endpoint": os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
        "azure_search_api_key": os.getenv("AZURE_SEARCH_API_KEY"),
        "index_name": index_name,
        "dimensions": 384,
        "model": os.getenv("MODEL")
    }
    vn_instance = MyVanna(config=config)
    vn_instance = connect_to_snowflake(vn_instance)
    return VannaTrainer(vn_instance)

@router.post("/train_base_data")
def train_base_data(
    index_name: str = Query(..., description="Azure Search index name"),
) -> schemas.TrainingResponse:
    trainer = create_trainer(index_name)
    try:
        trainer.train_base_data()
        return schemas.TrainingResponse(message="Successfully trained on base data.", record_id=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train_info_schema")
def train_info_schema(
    index_name: str = Query(...),
) -> schemas.TrainingResponse:
    trainer = create_trainer(index_name)
    try:
        trainer.train_data_info_schema()
        return schemas.TrainingResponse(message="Successfully trained on information schema.", record_id=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train_documents")
def train_documents(
    docs_request: schemas.TrainDocumentsRequest,
    index_name: str = Query(...),
) -> schemas.TrainingResponse:
    trainer = create_trainer(index_name)
    try:
        record_id = trainer.train_data_documents(docs_request.document)
        return schemas.TrainingResponse(message="Successfully trained on business documents.", record_id=record_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train_prompt_sql_pairs")
def train_prompt_sql_pairs(
    pairs_request: schemas.TrainPromptSQLPairsRequest,
    index_name: str = Query(...)
) -> schemas.TrainingResponse:
    trainer = create_trainer(index_name)
    try:
        record_id = trainer.train_data_prompt_sql_pairs(pairs_request.question, pairs_request.sql)
        return schemas.TrainingResponse(message="Successfully trained on prompt/sql pairs.", record_id=record_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train_ddl")
def train_ddl(
    index_name: str = Query(...),
):
    trainer = create_trainer(index_name)
    try:
        trainer.train_data_ddl()
        return {"message": "Successfully trained on DDL (if implemented)."}
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Training on DDL is not implemented yet.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_training_data")
def get_training_data(
    index_name: str = Query(...),
):
    trainer = create_trainer(index_name)
    try:
        training_data = trainer.get_training_data()
        return {"training_data": training_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
