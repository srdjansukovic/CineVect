from configparser import ConfigParser
import os
import weaviate
from weaviate.exceptions import UnexpectedStatusCodeException

parser = ConfigParser()
parser.read('./config/configuration.ini')

weaviate_client_url = parser.get('weaviate', 'client_url', vars=os.environ)
weaviate_api_key = parser.get('weaviate', 'api_key', vars=os.environ)
auth_config = weaviate.AuthApiKey(api_key=weaviate_api_key)

client = weaviate.Client(
    url = weaviate_client_url,
    auth_client_secret=auth_config
)

class_obj = {
    "class": "Movie",
    "vectorizer": "none",
    "properties": [
        {
            "name": "genre",
            "dataType": ["text[]"],
        },
        {
            "name": "year",
            "dataType": ["int"],
        },
        {
            "name": "origin",
            "dataType": ["text"],
        },
        {
            "name": "cast",
            "dataType": ["text[]"],
        },
        {
            "name": "director",
            "dataType": ["text[]"],
        }
    ]
}

try:
  client.schema.create_class(class_obj)
  print(f'Created new class {class_obj["class"]}')
except UnexpectedStatusCodeException:
  pass