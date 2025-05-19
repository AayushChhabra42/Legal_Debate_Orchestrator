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

class PlaintiffInput(BaseModel):
    transcript: list
    retrieved_cases: list

@app.post("/generate")
def generate_argument(data: PlaintiffInput):
    last_exchange = data.transcript if data.transcript else ""

    prompt = f"""
    You are a seasoned plaintiff attorney preparing an opening or rebuttal argument.

    Transcript of the courtroom so far:
    {data.transcript}

    Retrieved Precedent Cases:
    {data.retrieved_cases}

    Based on the facts, legal precedents, and prior exchanges,
    generate a persuasive and well-reasoned legal argument supporting the plaintiff's position.
    Highlight relevant statutes or rulings and strategically counter any opposing points.
    """

    # Stub: Replace this with a call to Vertex AI or other LLM
    argument = f"Plaintiff responds with a structured argument referencing case: {data.retrieved_cases[0]}"

    response = client.models.generate_content(
        model=model,
        contents=argument
    )


    return {"argument": response.text}