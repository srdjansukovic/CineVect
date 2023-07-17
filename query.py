from configuration import model, index

sentences = [
    {
        "id": "1",
        "text": "Mind twisting science fiction movie.",
        "metadata": {"genre": "Science Fiction", "year": 2010}
    }
]

embeddings = model.encode([sentence["text"] for sentence in sentences]).tolist()

query_response = index.query(
    vector=embeddings[0],
    filter={
        "genre": {"$eq": "Science Fiction"},
        "year": 2010
    },
    top_k=1,
    include_metadata=True
)

print(query_response)