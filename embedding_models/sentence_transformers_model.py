from sentence_transformers import SentenceTransformer
from configparser import ConfigParser
import os

parser = ConfigParser()
parser.read('./config/configuration.ini')

model_path = parser.get('sentence-transformers', 'model', vars=os.environ)

# all-MiniLM-L6-v2 maps sentences & paragraphs to a 384 dimensional dense vector space and
# all-mpnet-base-v2 maps sentences & paragraphs to a 768 dimensional dense vector space and
model = SentenceTransformer(model_path)