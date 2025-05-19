from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types
import os

app = FastAPI()

project_id=os.environ.get("PROJECT_ID")
location=os.environ.get("LOCATION")

client = genai.Client(
  vertexai=True, project=project_id, location=location,
)

model = "gemini-2.5-flash-preview-04-17"

class DefendantInput(BaseModel):
    transcript: list
    retrieved_cases: list

@app.post("/generate")
def generate_argument(data: DefendantInput):
    # Construct a detailed prompt for the defendant agent
    last_statement = data.transcript[-1]["text"] if data.transcript else ""
    prompt = f"""
    You are the legal counsel for the defendant in a simulated courtroom debate.
    Analyze the latest argument made by the plaintiff:
    "{last_statement}"

    Use the following relevant precedent cases to build your rebuttal:
    {data.retrieved_cases}

    Your goal is to defend your client convincingly by referencing applicable legal principles,
    contrasting case outcomes, and dismantling the plaintiff's position with logic and precedence.

    Provide a clear and persuasive counter-argument.
    """
    
    # Stub logic: Replace with actual LLM call or template rendering
    argument = f"Defendant responds to: '{last_statement}' using case {data.retrieved_cases}"
    response = client.models.generate_content(
        model=model,
        contents=argument
    )

    return {"defendant_argument": response.text}