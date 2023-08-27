from pinecone_db.pinecone_client import index
from models.sentence_transformers import model
from weaviate_db.weaviate_client import client as weaviate_client

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
    base_query = (
        weaviate_client.query
            .get("Movie", ["title", "year", "genre", "origin", "cast", "director"])
            .with_near_vector({
                "vector": embedding
            })
            .with_additional(["certainty"])
            .with_limit(n_results)
    )
    
    if filter["operands"]:
        response = base_query.with_where(filter).do()
    else:
        response = base_query.do()
        
    return response