from qdrant_db.qdrant_client import qdrant

qdrant.delete_collection(collection_name="movies")