from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from database import supabase
from models import QueryRequest, QueryResponse, Resource
import json

app = FastAPI(title="Learn with Jiji", description="AI Learning Companion Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for demo purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock AI Logic
def generate_mock_answer(query: str) -> str:
    query_lower = query.lower()
    if "rag" in query_lower:
        return "Retrieval-Augmented Generation (RAG) is a technique for enhancing the accuracy and reliability of generative AI models with facts fetched from external sources."
    elif "supabase" in query_lower:
        return "Supabase is an open source Firebase alternative. It provides a Postgres database, Authentication, instant APIs, Edge Functions, Realtime subscriptions, and Storage."
    else:
        return f"That's an interesting question about '{query}'. Here are some resources that might help you learn more."

@app.post("/ask-jiji", response_model=QueryResponse)
async def ask_jiji(request: QueryRequest, Authorization: Optional[str] = Header(None)):
    
    # Simple Mock Auth: Extract user_id from token if present, else use a mock ID
    # In a real app, verify the JWT properly.
    user_id = None
    if Authorization:
         # Simulating token decoding - assuming "Bearer <token>"
         # For this assignment, we'll pretend the token IS the user_id or just mock it.
         parts = Authorization.split(" ")
         if len(parts) == 2:
             # In production: Verify JWT
             pass
    
    # If no valid user (or for this demo), we can either fail or use a default mock ID for the database log
    # user_id = "mock-user-id" 

    try:
        # 1. Generate Answer (Mock AI)
        answer_text = generate_mock_answer(request.query)

        # 2. Search Resources in Supabase
        # Simple keyword search on title or description
        # Using Supabase 'ilike' for simple search
        terms = request.query.split()
        
        # Start with a basic query
        db_query = supabase.table("resources").select("*")
        
        # Very simple search logic: if any term matches title (logic can be improved)
        # For this demo, let's just fetch all and filter in python if needed, or use a simple text search if enabled.
        # Let's try to match the first significant word for simplicity or just fetch all for valid demo context
        
        # Fetching top 5 resources for simplicity of the "Search" simulation
        response = db_query.limit(5).execute()
        all_resources = response.data
        
        relevant_resources = []
        for res in all_resources:
            # Simple client-side filtering since we don't have full text search setup in SQL script yet
            if any(term.lower() in res['title'].lower() or term.lower() in (res.get('description') or '').lower() for term in terms):
                relevant_resources.append(res)
        
        # If no relevant found, just return 'Introduction to RAG' as a fallback for the demo if it exists
        if not relevant_resources and all_resources:
            relevant_resources = [all_resources[0]]

        # 3. Log the Query
        # Note: If RLS is enabled and we are not using a service key or valid user token, this might fail if the policy requires auth.
        # We will attempt to insert. If it fails due to RLS/Auth, we log a warning but don't fail the request for the user.
        try:
             # For the assignment, we might not have a signed-in user, so we might need to skip this 
             # OR we should have setup the table to allow public insert for the demo.
             # Our Setup.sql allowed insert for authenticated users.
             # Let's skip insertion if no user_id to avoid 500 errors during simple testing, 
             # OR we can try to insert if we have a mocked user_id.
             pass 
             # query_log = {
             #     "query_text": request.query,
             #     "response_json": {"answer": answer_text, "resources": relevant_resources},
             #     "user_id": user_id 
             # }
             # supabase.table("queries").insert(query_log).execute()
        except Exception as e:
            print(f"Warning: Failed to log query: {e}")

        return QueryResponse(
            answer=answer_text,
            resources=[Resource(**r) for r in relevant_resources]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "Welcome to Learn with Jiji API. Use POST /ask-jiji to start learning."}
