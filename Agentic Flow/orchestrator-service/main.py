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