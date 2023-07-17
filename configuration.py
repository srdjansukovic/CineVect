from sentence_transformers import SentenceTransformer
import pinecone

pinecone.init(api_key="", environment="asia-southeast1-gcp-free")
index = pinecone.Index("cinevect")

# all-MiniLM-L6-v2 maps sentences & paragraphs to a 384 dimensional dense vector space and
model = SentenceTransformer('all-MiniLM-L6-v2')