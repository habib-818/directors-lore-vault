import chromadb

# --- 1. BUILD THE FILING CABINET ---
# Initialize the ChromaDB client (this creates a database in your computer's RAM)
client = chromadb.Client()

# Create a specific collection (like a table or folder) to hold your YouTube scripts
collection = client.create_collection(name="youtube_scripts")

# --- 2. THE ARCHIVES (Your Chunked Data) ---
# Imagine your Python editor already sliced your massive PDF into these 3 chunks
script_chunks = [
    "In Phase 1 of our AI roadmap, we focused heavily on Python OOP, FastAPI, and Git version control.",
    "For video editing, the director prefers cinematic, dark moody lighting with a 50mm lens.",
    "During Phase 2, we mastered the Hugging Face pipeline, DataLoader padding, and the PyTorch 4-line training loop."
]

# --- 3. STORE THE CHUNKS (Embed & Save) ---
# You pass the English text directly to ChromaDB. 
# It automatically translates them into math coordinates and saves them.
# You must give every chunk a unique ID.
collection.add(
    documents=script_chunks,
    metadatas=[{"source": "roadmap_doc"}, {"source": "lighting_doc"}, {"source": "pytorch_doc"}],
    ids=["chunk_1", "chunk_2", "chunk_3"]
)
print("Data embedded and saved to the Vector Database!")

# --- 4. THE USER'S QUESTION ---
my_question = "What exactly did we learn how to do in Phase 2?"

# --- 5. THE SEARCH ENGINE (Retrieval) ---
# ChromaDB translates your question to a coordinate, finds the closest chunks, and returns them.
# n_results=1 means we only want the single best matching chunk.
results = collection.query(
    query_texts=[my_question],
    n_results=1
)

# Extract the winning text from the database output
best_chunk = results['documents'][0][0]
print(f"\nRetrieved Chunk: {best_chunk}")

# --- 6. THE TELEPROMPTER (Augmented Generation) ---
# We glue the retrieved chunk and the user's question together into a strict Master Prompt.
master_prompt = f"""
System: You are an AI assistant. Answer the user's question using ONLY the provided context.

Context: 
{best_chunk}

User Question: {my_question}
"""

print("\n--- Sending this to the LLM ---")
print(master_prompt)

# (In production, you would now pass 'master_prompt' to an LLM like ChatGPT or Llama to get the final answer)