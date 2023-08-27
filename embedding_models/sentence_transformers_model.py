from sentence_transformers import SentenceTransformer

# all-MiniLM-L6-v2 maps sentences & paragraphs to a 384 dimensional dense vector space and
model = SentenceTransformer('all-MiniLM-L6-v2')