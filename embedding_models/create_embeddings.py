import pandas as pd
from sentence_transformers_model import model
import json


df = pd.read_csv(filepath_or_buffer='data/clean_movies_mini.csv')
df = df.reset_index() 

print('Loaded file...')

embeddings = model.encode(sentences=[row['Title'] + '\n' + row['Plot'] for _, row in df.iterrows()], show_progress_bar=True).tolist()

embeddings_path = 'data/embeddings-with-title-mini.json'
with open(embeddings_path, 'w') as json_file:
  json.dump(embeddings, json_file, indent=4)