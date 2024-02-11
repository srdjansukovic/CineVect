import json
import pandas as pd
from weaviate_client import client
from weaviate.util import generate_uuid5

df = pd.read_csv(filepath_or_buffer='data/clean_movies.csv')
df = df.reset_index() 

print('Done with loading dataframe')

with open('data/embeddings-with-title.json', 'r') as json_file:
    embeddings = json.load(json_file)

print('Done with loading embeddings')

client.batch.configure(batch_size=100)
with client.batch as batch:  
    for index, row in df.iterrows():
        properties = {
            "genre": row['Genre'].split(','),
            "year": row['Release Year'],
            "origin": row['Origin/Ethnicity'],
            "cast": row['Cast'].split(','),
            "director": row['Director'].split(','),
            "title": row['Title']
        }
        batch.add_data_object(
            data_object=properties,
            class_name='Movie',
            vector=embeddings[index],
            uuid=generate_uuid5(properties)
        )

print('Done with importing data')