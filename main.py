from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import get_response
from database import save_message, get_history

app = FastAPI(title="Study Bot API", description="AI-powered Study Assistant with memory")


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    user_message: str
    bot_response: str


@app.get("/")
def root():
    return {"message": "Study Bot API is running!", "docs": "/docs"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Retrieve chat history for context
    history = get_history(request.session_id)

    # Get response from LLM
    bot_response = get_response(request.message, history)

    # Save the exchange to MongoDB
    save_message(request.session_id, request.message, bot_response)

    return ChatResponse(
        session_id=request.session_id,
        user_message=request.message,
        bot_response=bot_response
    )


@app.get("/history/{session_id}")
def chat_history(session_id: str):
    history = get_history(session_id)
    return {"session_id": session_id, "history": history}


@app.delete("/history/{session_id}")
def clear_history(session_id: str):
    from database import clear_session
    clear_session(session_id)
    return {"message": f"History cleared for session {session_id}"}
