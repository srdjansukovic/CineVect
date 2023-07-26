from configuration import model, index

sentences = [
    {
        "id": "1",
        "text": "moon and hats",
        "metadata": {"genre": "Unknown", "year": 1901}
    }
]

embeddings = model.encode([sentence["text"] for sentence in sentences]).tolist()

query_response = index.query(
    vector=embeddings[0],
    filter={
        "genre": {"$eq": "unknown"},
        "year": 1901
    },
    top_k=1,
    include_metadata=True
)

print(query_response)