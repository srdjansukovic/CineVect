import pandas as pd
from configuration import model, index
from data_preprocessing import df

df = df.reset_index() 

# TODO improve iterating over pandas dataframe
embeddings = model.encode([row['Plot'] for _ ,row in df.iterrows()]).tolist()

df = df.reset_index() 

sentence_tuples = [(row["Title"], embeddings[i], {"genre": row['Genre'], "year": row['Release Year'], "origin": row['Origin/Ethnicity']}) for i, row in df.iterrows()]

for _, row in df.iterrows():
  print(row['Plot'], row['Genre'], row['Release Year'])
  print('---------------------------------')

index.upsert(vectors=sentence_tuples, batch_size=5)

