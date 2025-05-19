from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/retrieve")
def retrieve(query: Query):
    # Replace this stub with Vertex AI Vector Search logic
    return ["case_001", "case_002"] 