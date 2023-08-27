from weaviate_client import client

client.schema.delete_class("Movie")