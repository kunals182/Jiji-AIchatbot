# Learn with Jiji - AI Learning Companion

This project implements the backend and frontend for "Learn with Jiji", an AI-driven learning companion.

## 🚀 Quick Setup

### 1. Backend (FastAPI)
```bash
# Install dependencies
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Run Server (http://127.0.0.1:8000)
fastapi dev main.py
```

### 2. Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
# App runs at http://localhost:5173
```

## 🗄️ Database Setup (Supabase)
1. Create a Supabase project and get your `SUPABASE_URL` and `SUPABASE_KEY` (Anon).
2. Add them to a `.env` file in the root directory.
3. Run the SQL script in `setup.sql` in your Supabase SQL Editor to create the necessary tables (`resources`, `queries`) and policies.

## 📡 API Endpoint
**POST** `/ask-jiji`
```json
{ "query": "Explain RAG" }
```
Returns a mocked AI answer + relevant learning resources (PPT/Video).

## 🎥 Demo Video
[**Click here to watch the demo video**](demo_video.mp4)

Open the frontend at `http://localhost:5173`, type a query like "Supabase", and see the results!
