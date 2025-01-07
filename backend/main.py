from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from load_models import ModelLoader
from judge import Judge
from openai import OpenAI
from dotenv import load_dotenv
import asyncio
import os 
import logging 

logging.basicConfig(level=logging.INFO)


load_dotenv()

app = FastAPI()
loader = ModelLoader()

openai_key = os.getenv('OPENAI_API_KEY')
if not openai_key:
    raise EnvironmentError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
openai_client = OpenAI(api_key=openai_key)
judge = Judge(client = openai_client)

class PromptRequest(BaseModel):
    task: str
    prompt: str


@app.on_event("startup")
async def startup_event():
    await loader.initialize_models()


@app.post("/generate/")
async def generate(prompt_request: PromptRequest):
    user_task = prompt_request.task
    user_input = prompt_request.prompt
    responses = {}

    try:
        # Collect responses from all models
        for provider, models in loader.available_models.items():
            for model_name in models:
                try:
                    if provider == "openai":
                        output = loader.openai(model_name, user_input, user_task)
                    elif provider == "gemini":
                        output = loader.gemini(model_name, user_input, user_task)
                    elif provider == "groq":
                        output = loader.groq(model_name, user_input, user_task)
                    elif provider == "claude":
                        output = loader.claude(model_name, user_input, user_task)
                    else:
                        output = "Provider not recognized."
                except Exception as e:
                    output = f"Error fetching response from {provider}-{model_name}: {str(e)}"
                responses[f"{provider}-{model_name}"] = output

        # Evaluate responses
        evaluations = {}
        scores = {}
        for model, response in responses.items():
            evaluation = await judge.g_eval(prompt_request.prompt, prompt_request.task, response)
            evaluations[model] = evaluation

            # Calculate average score
            scores[model] = sum(detail["score"] for detail in evaluation.values()) / len(evaluation)

        # Determine best model
        best_model = max(scores, key=scores.get)
        best_score = scores[best_model]

        # Return data for frontend
        return {
            "responses": responses,
            "evaluations": evaluations,
            "best_model": best_model,
            "best_score": float(best_score),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

