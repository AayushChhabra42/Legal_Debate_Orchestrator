# This response includes microservice templates (FastAPI + Docker) for GCP deployment using Cloud Run.
# We'll include the following services:
# - orchestrator-service
# - retriever-service
# - plaintiff-agent-service
# - defendant-agent-service
# - judge-agent-service
#
# Each folder will contain:
# - main.py (FastAPI logic)
# - requirements.txt
# - Dockerfile


# ------------- /orchestrator-service/main.py -------------
from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx

app = FastAPI()

PLAINTIFF_URL = "http://plaintiff-agent-service/generate"
DEFENDANT_URL = "http://defendant-agent-service/generate"
RETRIEVER_URL = "http://retriever-service/retrieve"
JUDGE_URL = "http://judge-agent-service/judge"

class CaseInput(BaseModel):
    case_facts: str

@app.post("/run")
async def run_case(case: CaseInput):
    transcript = []
    async with httpx.AsyncClient() as client:
        for _ in range(5):
            retrieved = (await client.post(RETRIEVER_URL, json={"query": case.case_facts})).json()

            p_args = {"case_facts": case.case_facts, "transcript": transcript, "retrieved_cases": retrieved}
            plaintiff = (await client.post(PLAINTIFF_URL, json=p_args)).json()["argument"]
            transcript.append({"role": "Plaintiff", "text": plaintiff})

            d_args = {"transcript": transcript, "retrieved_cases": retrieved}
            defendant = (await client.post(DEFENDANT_URL, json=d_args)).json()["argument"]
            transcript.append({"role": "Defendant", "text": defendant})

        judgment = (await client.post(JUDGE_URL, json={"transcript": transcript})).json()
        return {"judgment": judgment, "transcript": transcript}

# ------------- /retriever-service/main.py -------------
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/retrieve")
def retrieve(query: Query):
    # Replace this stub with Vertex AI Vector Search logic
    return ["case_001", "case_002"]

# ------------- /plaintiff-agent-service/main.py -------------
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PlaintiffInput(BaseModel):
    case_facts: str
    retrieved_cases: list
    transcript: list

@app.post("/generate")
def generate_argument(data: PlaintiffInput):
    prompt = f"""
    You are a plaintiff lawyer. Here are the facts:
    {data.case_facts}
    Context:
    {data.transcript}
    Cases:
    {data.retrieved_cases}
    Respond with your strongest argument.
    """
    return {"argument": f"Plaintiff says: Argument based on {data.retrieved_cases[0]}"}

# ------------- /defendant-agent-service/main.py -------------
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DefendantInput(BaseModel):
    transcript: list
    retrieved_cases: list

@app.post("/generate")
def generate_argument(data: DefendantInput):
    return {"argument": f"Defendant replies to {data.transcript[-1]['text']} with {data.retrieved_cases[1]}"}

# ------------- /judge-agent-service/main.py -------------
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class JudgeInput(BaseModel):
    transcript: list

@app.post("/judge")
def judge_case(data: JudgeInput):
    return {"verdict": "Plaintiff wins", "reasoning": "Better precedent cited."}

# ------------- Shared Files for Each Service -------------
# Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# requirements.txt
fastapi
uvicorn
httpx
pydantic

# ------------- GCP Deployment Plan -------------
# 1. Enable required APIs:
#    gcloud services enable run.googleapis.com artifactregistry.googleapis.com

# 2. Create Artifact Registry:
#    gcloud artifacts repositories create legal-agents --repository-format=docker --location=us-central1

# 3. For each service:
#    docker build -t us-central1-docker.pkg.dev/YOUR_PROJECT_ID/legal-agents/orchestrator-service .
#    docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/legal-agents/orchestrator-service

# 4. Deploy to Cloud Run:
#    gcloud run deploy orchestrator-service \
#        --image=us-central1-docker.pkg.dev/YOUR_PROJECT_ID/legal-agents/orchestrator-service \
#        --platform=managed --region=us-central1 --allow-unauthenticated

# Repeat this for all services.

# 5. Environment variables or Secret Manager can be used for API keys, URLs, etc.

# 6. Use Pub/Sub or Cloud Tasks if you want to asynchronously chain debate rounds with logging.

# Let me know if you want IaC (Terraform or YAML-based GCP deployment) next.
