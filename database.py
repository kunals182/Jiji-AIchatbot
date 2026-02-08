import os
from typing import List, Dict, Any, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file")

class SupabaseTable:
    def __init__(self, client: "SupabaseClient", table_name: str):
        self.client = client
        self.table_name = table_name

    def select(self, columns: str = "*", count: Optional[str] = None) -> "SupabaseQueryBuilder":
        return SupabaseQueryBuilder(self, method="GET", params={"select": columns})
    
    def insert(self, data: Dict[str, Any]) -> "SupabaseQueryBuilder":
         return SupabaseQueryBuilder(self, method="POST", json_data=data)

class SupabaseQueryBuilder:
    def __init__(self, table: SupabaseTable, method: str, params: Dict = None, json_data: Dict = None):
        self.table = table
        self.method = method
        self.params = params or {}
        self.json_data = json_data
        self.headers = table.client.headers.copy()
        if method == "POST":
            # Prefer return=representation to get back the inserted data
            self.headers["Prefer"] = "return=representation"

    def limit(self, count: int):
        self.params["limit"] = count
        return self

    def execute(self):
        url = f"{self.table.client.rest_url}/{self.table.table_name}"
        # Use sync client for simplicity in this synchronous flow, or could be async.
        # But fastapi async def handles sync calls in threadpool, or we use async client.
        # Let's use httpx.post/get directly which are sync wrappers.
        # Since ask_jiji is async, we should ideally use async client, but for simplicity sync is fine.
        
        response = httpx.request(
            method=self.method,
            url=url,
            headers=self.headers,
            params=self.params,
            json=self.json_data
        )
        response.raise_for_status()
        
        # Mocking the response object structure expected by main.py (response.data)
        class Response:
            pass
        r = Response()
        r.data = response.json()
        return r

class SupabaseClient:
    def __init__(self, url: str, key: str):
        # Remove trailing slash if present
        url = url.rstrip("/")
        self.rest_url = f"{url}/rest/v1"
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

    def table(self, table_name: str) -> SupabaseTable:
        return SupabaseTable(self, table_name)

supabase = SupabaseClient(url, key)
