from pydantic import BaseModel

class TrainingResponse(BaseModel):
    """
    Response for training endpoints
    """
    message: str
    record_id: str | None

class TrainDocumentsRequest(BaseModel):
    """
    Schema for /train_documents
    """
    document: str

class TrainPromptSQLPairsRequest(BaseModel):
    """
    Schema for /train_prompt_sql_pairs
    """
    question: str
    sql: str