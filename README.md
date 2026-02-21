# 📚 StudyBot - AI Study Assistant API

An AI-powered Study Bot built with FastAPI, LangChain, Groq LLM, and MongoDB. The bot answers academic questions and remembers previous conversations using database memory.

---

## 🚀 Features
- **Context-Aware Responses**: Remembers conversation history per session
- **MongoDB Memory**: Persists chat history in a local or cloud MongoDB database
- **Academic Focus**: Tuned system prompt for study-related questions
- **REST API**: Clean FastAPI endpoints with auto-generated docs at `/docs`
- **Deployable**: Render-ready configuration

---

## 🛠️ Setup Instructions
### Prerequisites
- Python 3.10+
- MongoDB (local) OR MongoDB Atlas account
- Groq API Key (free at https://console.groq.com)

### Step 1: Clone the Repository
```bash
git clone https://github.com/tawanda2020-wq/studybot
cd studybot
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv


### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Copy the env file
cp .env .env

# Edit .env and add your actual keys:
# GROQ_API_KEY=gsk_your_actual_key
# MONGO_URI=mongodb://localhost:27017
```

### Step 5: Start MongoDB (Local)
```bash

# On Windows: Start MongoDB service from Services or:
net start MongoDB
```

---

## ▶️ How to Run

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**

Interactive docs (Swagger UI): **http://localhost:8000/docs**

---

## 📡 API Endpoints

### POST `/chat`
Send a message to the study bot.

**Request Body:**
```json
{
  "session_id": "student_001",
  "message": "Explain the Pythagorean theorem"
}
```

**Response:**
```json
{
  "session_id": "student_001",
  "user_message": "Explain the Pythagorean theorem",
  "bot_response": "The Pythagorean theorem states that in a right triangle..."
}
```

### GET `/history/{session_id}`
Retrieve full conversation history for a session.

### DELETE `/history/{session_id}`
Clear conversation history for a session.

---

## ☁️ Deployment on Render

1. Push your code to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your GitHub repository
4. Set the **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add **Environment Variables** in Render dashboard:
   - `GROQ_API_KEY` = your Groq API key
   - `MONGO_URI` = your MongoDB Atlas connection string
6. Click **Deploy**

---

## 🗂️ Project Structure

```
studybot/
├── main.py          # FastAPI app and route handlers
├── chatbot.py       # LLM integration (Groq + LangChain)
├── database.py      # MongoDB connection and operations
├── requirements.txt # Python dependencies
├── .env             # Environment variable template
└── README.md        # This file
```

---

## 🧪 Testing the API

visit `http://localhost:8000/docs` for the interactive Swagger UI.
