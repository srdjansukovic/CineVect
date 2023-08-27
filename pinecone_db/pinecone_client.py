from configparser import ConfigParser
import os
import pinecone

parser = ConfigParser()
parser.read('./config/configuration.ini')

pinecone_api_key = parser.get('pinecone', 'api_key', vars=os.environ)
pinecone_environment = parser.get('pinecone', 'environment', vars=os.environ)
pinecone_index = parser.get('pinecone', 'index', vars=os.environ)
pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
index = pinecone.Index(index_name=pinecone_index)