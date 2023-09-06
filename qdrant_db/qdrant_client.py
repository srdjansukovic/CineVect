from qdrant_client import QdrantClient
from configparser import ConfigParser
import os

parser = ConfigParser()
parser.read('./config/configuration.ini')

qdrant_api_key = parser.get('qdrant', 'api_key', vars=os.environ)
qdrant_url = parser.get('qdrant', 'url', vars=os.environ)

qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)