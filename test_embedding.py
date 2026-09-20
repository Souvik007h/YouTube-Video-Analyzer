from src.embeddings import get_embedding_model


print("Loading embedding model...")

embeddings = get_embedding_model()

print("Creating embedding...")

vector = embeddings.embed_query(
    "How does Ethereum smart contract deployment work?"
)

print("\nEmbedding created successfully!")

print("Vector type:", type(vector))

print("Vector dimensions:", len(vector))

print("\nFirst 10 values:")

print(vector[:10])