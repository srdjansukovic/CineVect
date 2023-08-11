from configuration import model, index

# sentences = [
#     {
#         "id": "1",
#         "text": " The FBI raids and shuts down Stratton Oakmont. Despite this one breach, Jordan receives a reduced sentence for his testimony and serves three years in a minimum security prison.",
#         "metadata": {"genre": "Unknown", "year": 1901}
#     }
# ]

# embeddings = model.encode([sentence["text"] for sentence in sentences]).tolist()

# query_response = index.query(
#     vector=embeddings[0],
#     filter={
#         "genre": {"$eq": "Comedy"}
#     },
#     top_k=3,
#     include_metadata=True
# )

def create_embedding_from_query(query):
    return model.encode(query).tolist()

def query_search(embedding, filter, n_results):
    return index.query(
        vector=embedding,
        filter=filter,
        top_k=n_results,
        include_metadata=True
    )
