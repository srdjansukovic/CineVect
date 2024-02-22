from transformers import BartForConditionalGeneration, BartTokenizer
from sentence_transformers import SentenceTransformer
from configparser import ConfigParser
import os
import pinecone
import csv

def read_csv_to_map(csv_file):
    title_to_plot = {}
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row['Title']
            plot = row['Plot']
            title_to_plot[title] = plot
    return title_to_plot

csv_file = './data/clean_movies_mini.csv'
title_to_plot = read_csv_to_map(csv_file)

parser = ConfigParser()
parser.read('./config/configuration.ini')

pinecone_api_key = parser.get('pinecone', 'api_key', vars=os.environ)
pinecone_environment = parser.get('pinecone', 'environment', vars=os.environ)
pinecone_index = parser.get('pinecone', 'index', vars=os.environ)
pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
index = pinecone.Index(index_name=pinecone_index)

def pinecone_query(embedding, filter, n_results):
    return index.query(
        vector=embedding,
        filter=filter,
        top_k=n_results,
        include_metadata=True
    )

sentence_transformer = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
def create_embedding_from_query(query):
    return sentence_transformer.encode(query).tolist()

paraphrase_model = BartForConditionalGeneration.from_pretrained('eugenesiow/bart-paraphrase')
tokenizer = BartTokenizer.from_pretrained('eugenesiow/bart-paraphrase')

def paraphrase(input_sentence, max_input_length=512, max_output_length=512):
    input_ids = tokenizer.encode(input_sentence, return_tensors='pt', max_length=max_input_length, truncation=True)
    generated_ids = paraphrase_model.generate(input_ids, max_length=max_output_length, num_beams=4, early_stopping=True)
    paraphrase_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    
    return paraphrase_text

def calculate_metrics(total_valid_guesses, total_invalid_guesses):
    if total_valid_guesses + total_invalid_guesses != 0:
        precision = total_valid_guesses / (total_valid_guesses + total_invalid_guesses)
    else:
        precision = 0.0
    
    actual_positives = total_valid_guesses 
    if actual_positives != 0:
        recall = total_valid_guesses / actual_positives
    else:
        recall = 0.0
    
    if precision + recall != 0:
        f1_score = 2 * (precision * recall) / (precision + recall)
    else:
        f1_score = 0.0

    return precision, recall, f1_score

valid_guesses = 0
invalid_guesses = 0
for title, plot in title_to_plot.items():
    paraphrased_plot = paraphrase(plot)
    embedding = create_embedding_from_query(paraphrased_plot)
    query_response = pinecone_query(embedding=embedding, filter=None, n_results=1)
    query_response_dict = query_response.to_dict()
    matched_title = query_response_dict['matches'][0]['id'].split(' (')[0]
    if title == matched_title:
        valid_guesses += 1
    else:
        invalid_guesses += 1

print('Test results: ')
print('Valid guesses: ', valid_guesses)
print('Invalid guesses: ', invalid_guesses)

precision, recall, f1_score = calculate_metrics(valid_guesses, invalid_guesses)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1_score)





