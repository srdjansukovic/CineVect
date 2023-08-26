from configparser import ConfigParser
import os
from sentence_transformers import SentenceTransformer
import pinecone

parser = ConfigParser()
parser.read('./configuration.ini')

pinecone_api_key = parser.get('pinecone', 'api_key', vars=os.environ)
pinecone_environment = parser.get('pinecone', 'environment', vars=os.environ)
pinecone_index = parser.get('pinecone', 'index', vars=os.environ)
pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
index = pinecone.Index(index_name=pinecone_index)

# all-MiniLM-L6-v2 maps sentences & paragraphs to a 384 dimensional dense vector space and
model = SentenceTransformer('all-MiniLM-L6-v2')
