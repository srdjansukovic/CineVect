docker-build:
	@docker build -t cinevect:latest .

create-embeddings:
	@python embedding_models/create_embeddings.py

weaviate-indexing:
	@python weaviate_db/weaviate_indexing.py

weaviate-cleanup:
	@python weaviate_db/weaviate_cleanup.py

pinecone-indexing:
	@python pinecone_db/pinecone_indexing.py

pinecone-cleanup:
	@python pinecone_db/pinecone_cleanup.py

qdrant-indexing:
	@python qdrant_db/qdrant_indexing.py

qdrant-cleanup:
	@python qdrant_db/qdrant_cleanup.py