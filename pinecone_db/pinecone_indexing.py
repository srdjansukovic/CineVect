import pandas as pd
from pinecone_client import index
import json

df = pd.read_csv(filepath_or_buffer='data/clean_movies.csv')
df = df.reset_index() 

print('Done with loading dataframe')

with open('data/embeddings-with-title.json', 'r') as json_file:
    embeddings = json.load(json_file)

print('Done with loading embeddings')

df = df.reset_index() 

sentence_tuples = [(f"{row['Title']} ({row['Release Year']})", embeddings[i], {"genre": row['Genre'].split(','), "year": row['Release Year'], "origin": row['Origin/Ethnicity'], "cast": row['Cast'].split(','), "director": row['Director'].split(',')}) for i, row in df.iterrows()]

print('Created sentence tuples for pinecone indexing...')

index.upsert(vectors=sentence_tuples, batch_size=200, show_progress=True)

print('Done with indexing...')

