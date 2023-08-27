docker-build:
	@docker build -t cinevect:latest .

run-weaviate:
	@docker compose up weaviate

weaviate-indexing:
	@python weaviate_db/weaviate_indexing.py

weaviate-cleanup:
	@python weaviate_db/weaviate_cleanup.py

pinecone-indexing:
	@python pinecone_db/pinecone_indexing.py

pinecone-cleanup:
	@python pinecone_db/pinecone_cleanup.py