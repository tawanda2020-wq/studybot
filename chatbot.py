import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage, AIMessage

load_dotenv()  # ← This loads .env file

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """You are StudyBot, an intelligent and friendly AI study assistant. 
Your role is to help students learn and understand academic topics effectively.

Guidelines:
- Answer study-related questions clearly and concisely
- Break down complex concepts into easy-to-understand steps
- Provide examples where helpful
- If asked about non-study topics, gently redirect to academic subjects
- Encourage good study habits and learning
- Remember context from previous messages in the conversation
- Support subjects including Math, Science, History, Literature, Programming, and more

Always be encouraging, patient, and educational in your responses."""


def get_response(user_message: str, history: list) -> str:
    """
    Generate a response from the LLM using conversation history for context.
    
    Args:
        user_message: The current user input
        history: List of previous messages [{"role": "user/assistant", "content": "..."}]
    
    Returns:
        Bot response string
    """
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=1024
    )

    # Build message list with system prompt
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    # Add conversation history for context (last 10 exchanges to avoid token limits)
    for msg in history[-20:]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    # Add current user message
    messages.append(HumanMessage(content=user_message))

    # Get response from LLM
    response = llm.invoke(messages)
    return response.content
