import pandas as pd
from configuration import model, index
import json


df = pd.read_csv(filepath_or_buffer='data/clean_movies.csv')
df = df.reset_index() 

print('Loaded file...')

embeddings = model.encode([row['Plot'] for _ ,row in df.iterrows()]).tolist()

embeddings_path = 'data/embeddings.json'
with open(embeddings_path, 'w') as json_file:
  json.dump(embeddings, json_file, indent=4)

print('Done with creating embeddings...')

df = df.reset_index() 

sentence_tuples = [(f"{row['Title']} ({row['Release Year']})", embeddings[i], {"genre": row['Genre'].split(','), "year": row['Release Year'], "origin": row['Origin/Ethnicity'], "cast": row['Cast'].split(','), "director": row['Director'].split(',')}) for i, row in df.iterrows()]

print('Created sentence tuples for pinecone indexing...')

index.upsert(vectors=sentence_tuples, batch_size=200)

print('Done with indexing...')

