import chromadb

print("🎬 Booting up the Search Engine...")

# --- 1. CONNECT TO THE HARD DRIVE ---
# We point Chroma right back to the exact same folder we just built.
# Because the 79MB translator is already cached, this will load instantly.
client = chromadb.PersistentClient(path="./lore_vault_db")

# --- 2. OPEN THE TABLE ---
# Notice we use 'get_collection' this time, NOT 'create'. 
# We just want to read the existing table, not build a new one.
collection = client.get_collection(name="youtube_lore")

# --- 3. THE DIRECTOR'S QUESTION ---
# Let's ask it about your cinematography style instead of the roadmap.
my_question = "What kind of lighting and camera lens should I use for my next video?"

print(f"🔍 Searching the vault for: '{my_question}'...\n")

# --- 4. RETRIEVAL (The Search) ---
results = collection.query(
    query_texts=[my_question],
    n_results=1
)

# Extracting the actual text from the double-list packaging
best_chunk = results['documents'][0][0]

# --- 5. THE TELEPROMPTER ---
master_prompt = f"""
System: You are an elite AI assistant for a YouTube Director. Answer the user's question using ONLY the provided context. Do not invent answers.

Context: 
{best_chunk}

User Question: {my_question}
"""

print("--- 📜 FINAL TELEPROMPTER OUTPUT ---")
print(master_prompt)