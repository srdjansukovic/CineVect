from configuration import model, index
from weaviate_client import client as weaviate_client

def create_embedding_from_query(query):
    return model.encode(query).tolist()

def pinecone_query(embedding, filter, n_results):
    return index.query(
        vector=embedding,
        filter=filter,
        top_k=n_results,
        include_metadata=True
    )

def weaviate_query(embedding, filter, n_results):
    response = (
        weaviate_client.query
            .get("Movie", ["title", "year", "genre", "origin", "cast", "director"])
            .with_where(filter)
            .with_near_vector({
                "vector": embedding
            })
            .with_additional(["certainty"])
            .with_limit(n_results)
            .do()
    )
    return response