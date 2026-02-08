# Learn with Jiji - Backend Service

This is the backend service for "Learn with Jiji", an AI-driven learning companion, built for the VeidaLabs Software Developer Hiring Assignment.

## Features
- **FastAPI**: High-performance, easy-to-learn, fast-to-code, ready-for-production web framework.
- **Supabase Integration**: Uses Supabase for Database and Authentication (simulated).
- **Mocked AI**: Simulates AI response generation for demonstration purposes.
- **RLS**: Row Level Security policies defined in SQL.

## Prerequisites
- Python 3.8+
- Supabase Account

## Setup Instructions

1.  **Clone/Download the repository** (if applicable).
2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables**:
    - Rename `.env.example` to `.env` (or create `.env` if missing).
    - Add your Supabase credentials:
      ```
      SUPABASE_URL=your_supabase_project_url
      SUPABASE_KEY=your_supabase_anon_key
      ```
      ```
5.  **Setup Database & Storage**:
    - Go to your [Supabase Dashboard](https://supabase.com/dashboard) -> SQL Editor.
    - Copy the contents of `setup.sql` and run it.
    - This will:
        - Create `resources` and `queries` tables.
        - Create a `content_files` Storage bucket (for your PPT/Video files).
        - Insert sample data.
    - **Optional**: Go to "Storage" in Supabase, open `content_files`, and upload your own PPT/Video files. Then update the `url` in the `resources` table to point to your real files.
6.  **Setup Frontend (Optional but Recommended)**:
    ```bash
    cd frontend
    npm install
    ```

## Running the Server

### Backend
```bash
# In the root folder
.\venv\Scripts\activate
fastapi dev main.py
```
Backend runs at `http://127.0.0.1:8000`.

### Frontend
```bash
# In the frontend folder
cd frontend
npm run dev
```
Frontend runs at `http://localhost:5173`.

## Recording the Demo Video
You have two options for the demo video:

### Option A: Using the React Frontend (Recommended for "WOW" factor)
1.  **Start Backend**: `fastapi dev main.py`
2.  **Start Frontend**:
    ```bash
    cd frontend
    npm run dev
    ```
3.  Open `http://localhost:5173`.
4.  Type "Explain RAG" and hit Enter.
5.  Show the beautiful response and resource cards.

### Option B: Using Swagger UI (Backend Only)
1.  Start the server: `fastapi dev main.py`
2.  Go to `http://127.0.0.1:8000/docs` in your browser.
3.  Expand `POST /ask-jiji`, click **Try it out**, enter JSON, and Execute.

## API Documentation

### `POST /ask-jiji`

Accepts a user query and returns a structured AI response with learning resources.

**Request Header**:
- `Authorization`: `Bearer <token>` (Optional for this demo, usually required)

**Request Body**:
```json
{
  "query": "Explain RAG"
}
```

**Response**:
```json
{
  "answer": "Retrieval-Augmented Generation (RAG) is...",
  "resources": [
    {
      "id": "...",
      "title": "Introduction to RAG",
      "type": "ppt",
      "url": "https://example.com/rag-intro.pptx",
      "description": "...",
      "tags": ["rag", "ai"]
    }
  ]
}
```

## Security & Architecture

### Supabase & RLS
- **Schema**:
    - `resources`: Publicly readable content.
    - `queries`: Stores user questions.
- **Row Level Security (RLS)**:
    - `resources`: Enabled. Policy `"Enable read access for all users"` allows public access.
    - `queries`: Enabled. Policies restrict users to see only their own queries (`auth.uid() = user_id`).
- **Auth**: The backend uses the `supabase-py` client. In a production scenario, the `Authorization` header would be verified against Supabase Auth to get the user ID.

### Improvements (with more time)
- **Real AI Integration**: Connect to OpenAI or Anthropic API to generate dynamic answers.
- **Vector Search**: Use `pgvector` in Supabase for semantic search of resources instead of keyword matching.
- **Strict Auth**: Implement full JWT verification middleware.
- **Caching**: Redis caching for frequent queries.
