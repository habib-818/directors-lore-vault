import chromadb
import os

print("🎬 Booting up the vault construction...")

# --- 1. THE PERMANENT HARD DRIVE CONNECTION ---
# Instead of RAM, we force ChromaDB to create a physical folder in your current directory.
client = chromadb.PersistentClient(path="./lore_vault_db")

# --- 2. CREATE THE COLLECTION (The Table) ---
# We use 'get_or_create' instead of 'create'. 
# Why? If you run this script twice, 'create' will crash. This safely opens it if it already exists.
collection = client.get_or_create_collection(name="youtube_lore")

# --- 3. THE RAW DATA (Your Scripts) ---
# In a massive production, you would use Python's 'os' module to read 100 different .txt files here.
# For this build, we are loading three core pieces of your lore.
lore_chunks = [
    "The Director's visual style relies heavily on high contrast, dark moody lighting, and a 50mm cinematic lens.",
    "Phase 1 of the AI Engineering roadmap focuses entirely on building infrastructure: Python OOP, FastAPI, and Git.",
    "Phase 2 of the AI roadmap is the ML Engine phase, covering PyTorch, Hugging Face, DataLoaders, and the 4-line training loop."
]

# We must provide exact serial numbers for each chunk
chunk_ids = ["lore_1", "lore_2", "lore_3"]

# Hidden sticky notes so you can filter searches later
chunk_metadata = [
    {"category": "cinematography"}, 
    {"category": "roadmap_phase_1"}, 
    {"category": "roadmap_phase_2"}
]

# --- 4. EMBED AND BURN TO DISK ---
print("⚙️ Translating English to Math and saving to hard drive...")

# This command sends the text to the Embedding Model, gets the coordinates, and saves everything to the folder.
# We use an 'upsert' command (Update + Insert). If 'lore_1' already exists, it safely overwrites it instead of crashing.
collection.upsert(
    documents=lore_chunks,
    metadatas=chunk_metadata,
    ids=chunk_ids
)

print("✅ Vault successfully built! Check your VS Code file explorer.")