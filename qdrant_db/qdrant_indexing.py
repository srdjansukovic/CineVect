from qdrant_clients import qdrant
from qdrant_client import models
import pandas as pd
import json

qdrant.recreate_collection(
    collection_name="movies",
    vectors_config=models.VectorParams(
        size=768,
        distance=models.Distance.COSINE
    )
)

df = pd.read_csv(filepath_or_buffer='data/clean_movies_mini.csv')
df = df.reset_index() 

print('Done with loading dataframe')

with open('data/embeddings-with-title-mini.json', 'r') as json_file:
    embeddings = json.load(json_file)

print('Done with loading embeddings')

qdrant.upload_records(
    collection_name="movies",
    records=[
        models.Record(
            id=index,
            vector=embeddings[index],
            payload={
                    "genre": row['Genre'].split(','),
                    "year": row['Release Year'],
                    "origin": row['Origin/Ethnicity'],
                    "cast": row['Cast'].split(','),
                    "director": row['Director'].split(','),
                    "title": row['Title']
                }
        ) for index, row in df.iterrows()
    ]
)