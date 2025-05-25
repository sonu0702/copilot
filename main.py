import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.agent_interaction_service import AgentInteractionService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NavDesk Copilot API (CrewAI Edition)",
    description="API to interact with the NavDesk Copilot agent (powered by CrewAI), specialized in Stripe.",
    version="1.0.0",
    docs_url="/docs", # Explicitly set docs URL
    redoc_url=None # Disable ReDoc if not needed
)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AnswerResponse)
async def ask_question_api(request: QuestionRequest):
    try:
        service = AgentInteractionService()
    except RuntimeError as e:
        logger.critical(f"Failed to initialize AgentInteractionService for /ask request: {e}", exc_info=True)
        raise HTTPException(status_code=503, detail=f"Service initialization failed.")

    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        answer = service.ask_stripe_expert(request.question)
        return AnswerResponse(answer=answer)
    except Exception as e:
        logger.error(f"Error in /ask endpoint for question '{request.question}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal error occurred.")

@app.get("/")
async def read_root():
    return {"message": "NavDesk Copilot API is running. Use /docs for API details."}

# The uvicorn.run block for direct execution is typically removed for production.
# Deployment should be handled by a process manager like Gunicorn with Uvicorn workers.
