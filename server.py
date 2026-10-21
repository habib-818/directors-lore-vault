from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb

print("🎬 Booting up the Lore Vault API Server...")

# --- 1. INITIALIZE THE SERVER & DATABASE ---
# We boot these up OUTSIDE the endpoint so they only load once when the server starts, not every time someone asks a question.
app = FastAPI(title="The Director's Lore Vault")
client = chromadb.PersistentClient(path="./lore_vault_db")
collection = client.get_collection(name="youtube_lore")

# --- 2. THE BLUEPRINT (Pydantic) ---
# We define exactly what the incoming JSON request must look like.
class UserRequest(BaseModel):
    question: str

# --- 3. THE ENDPOINT (The API Route) ---
@app.post("/ask")
async def ask_vault(request: UserRequest):
    print(f"🔍 Incoming transmission received: '{request.question}'")
    
    try:
        # Step A: Search the Vector Database
        results = collection.query(
            query_texts=[request.question],
            n_results=1
        )
        
        # Step B: Extract the winning chunk
        best_chunk = results['documents'][0][0]
        
        # Step C: Build the Teleprompter
        master_prompt = f"""
        System: You are an elite AI assistant for a YouTube Director. Answer using ONLY the provided context. Do not invent answers.

        Context: 
        {best_chunk}

        User Question: {request.question}
        """
        
        # Step D: Return the JSON response to the user
        return {
            "status": "success",
            "retrieved_context": best_chunk,
            "final_teleprompter": master_prompt
        }
        
    except Exception as e:
        # If anything crashes, we send a clean error message back instead of breaking the server.
        raise HTTPException(status_code=500, detail=str(e))