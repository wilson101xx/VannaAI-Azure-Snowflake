from fastapi import FastAPI
from src.api.routers import training, query

app = FastAPI()

# Include the routers
app.include_router(training.router)
app.include_router(query.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Vanna Training & Query API"}
