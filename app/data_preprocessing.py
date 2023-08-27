import pandas as pd
import json, re

df = pd.read_csv(filepath_or_buffer='data/movies.csv')
df = df.drop('Wiki Page', axis=1)
df = df.dropna()
# Drop rows where any column contains 'unknown' or 'Unknown'
df = df[~df.applymap(lambda x: 'unknown' in str(x).lower() if pd.notnull(x) else False).any(axis=1)]

unique_origins = df["Origin/Ethnicity"].unique().tolist()
origins_path = 'data/origins.json'
with open(origins_path, 'w') as json_file:
  json.dump(unique_origins, json_file, indent=4)

def split_and_join(s):
    parts = [x.strip() for x in re.split(',|and', s)]
    return ','.join(parts)

df['Cast'] = df['Cast'].apply(split_and_join)
df['Director'] = df['Director'].apply(split_and_join)

unique_actors = df['Cast'].str.split(r',').explode().str.strip().unique().tolist()
actors_path = 'data/actors.json'
with open(actors_path, 'w') as json_file:
  json.dump(unique_actors, json_file, indent=4)


unique_directors = df['Director'].str.split(r',').explode().str.strip().unique().tolist()
directors_path = 'data/directors.json'
with open(directors_path, 'w') as json_file:
  json.dump(unique_directors, json_file, indent=4)

movie_genres_mapping = {
    'Action': ['Action', 'adventure', 'Action-packed', 'gangster', 'swashbuckler', 'samurai', 'kung fu', 'kung-fu'],
    'Comedy': ['Comedy', 'Humor', 'Funny', 'parody', 'biodrama', 'slapstick'],
    'Drama': ['Drama', 'Tearjerker', 'melodrama', 'suspense', 'dramedy', 'docudrama', 'tragedy'],
    'Adventure': ['Adventure'],
    'Animation': ['Animation', 'Cartoon', 'Animated'],
    'Crime': ['Crime', 'Detective', 'Criminal'],
    'Documentary': ['Documentary', 'Non-fiction', 'Factual'],
    'Family': ['Family', 'Children', 'Kids'],
    'Fantasy': ['Fantasy', 'Magical'],
    'Horror': ['Horror', 'Scary', 'Spooky', 'Vampire', 'Slasher'],
    'Musical': ['Musical', 'Song-and-dance', 'Music', 'dance'],
    'Mystery': ['Mystery', 'Enigma', 'Puzzle'],
    'Romance': ['Romance', 'Love', 'Relationship', 'Romantic'],
    'Science Fiction': ['Science Fiction', 'Sci-Fi', 'Futuristic', 'science-fiction', 'sci fi', 'fiction', 'tokusatsu', 'wuxia'],
    'Thriller': ['Thriller', 'Suspenseful', 'Tense'],
    'War': ['War', 'Battle', 'Combat', 'world war', 'ww1', 'ww2'],
    'Western': ['Western', 'Cowboy', 'Wild West'],
    'Biographical': ['Biographical', 'Biopic', 'Real-life', 'biography', 'bio-pic', 'biographic'],
    'Historical': ['Historical', 'Period', 'Old-time', 'history', 'folklore', 'patriotic'],
    'Superhero': ['Superhero', 'Heroic', 'Supernatural'],
    'Sports': ['Sports', 'Athletic', 'Sporting', 'Sport'],
    'Spy': ['Spy', 'Espionage', 'Secret Agent'],
    'Supernatural': ['Supernatural', 'Paranormal', 'Otherworldly'],
    'Disaster': ['Disaster', 'Catastrophe', 'Apocalypse'],
    'Psychological': ['Psychological', 'Mental', 'Mind Games'],
    'Noir': ['Noir', 'Film Noir', 'Dark'],
    'Teen': ['Teen', 'Adolescent', 'Young'],
    'Coming of Age': ['Coming of Age', 'Growing Up', 'Coming-of-age'],
    'Animated Musical': ['Animated Musical', 'Cartoon Musical'],
    'Music': ['Music', 'Concert', 'Orchestra', 'operetta'],
    'Martial Arts': ['Martial Arts', 'Combat', 'Fighting'],
    'Silent': ['Silent', 'Mute', 'No Sound'],
    'Crime Thriller': ['Crime Thriller', 'Detective Thriller'],
    'Epic': ['Epic', 'Grand', 'Spectacular'],
    'Period Drama': ['Period Drama', 'Historical Drama'],
    'Satire': ['Satire', 'Mockery', 'Ironic'],
    'Political': ['Political', 'Politics', 'Government'],
    'Social Issues': ['Social Issues', 'Social Drama'],
    'Art House': ['Art House', 'Independent', 'Arthouse'],
    'Experimental': ['Experimental', 'Avant-Garde'],
    'Romantic Comedy': ['Romantic Comedy', 'Rom-Com', 'rom com'],
    'Cult': ['Cult', 'Cult Classic'],
    'Zombie': ['Zombie', 'Undead', 'Living Dead'],
    'Post-Apocalyptic': ['Post-Apocalyptic', 'Aftermath', 'Dystopian'],
    'Fantasy Adventure': ['Fantasy Adventure', 'Mythical Adventure'],
    'Time Travel': ['Time Travel', 'Time-travel'],
    'Cyberpunk': ['Cyberpunk', 'High Tech'],
    'Found Footage': ['Found Footage', 'First-Person'],
    'Mockumentary': ['Mockumentary', 'Fake Documentary'],
    'Western Comedy': ['Western Comedy', 'Cowboy Comedy'],
    'Short': ['short'],
    'Anime': ['anime'],
    'Mythology': ['mythology', 'mythological', 'religious', 'biblical', 'devotional', 'christian'],
    'Social': ['social'],
    'Serial': ['serial', 'anthology'],
    'Masala': ['masala']

}

def extract_genres(genre_string):
    genres = []
    for standard_genre, synonyms in movie_genres_mapping.items():
        pattern = r'\b(?:' + '|'.join(synonyms) + r')\b'
        if re.search(pattern, genre_string, re.IGNORECASE):
            genres.append(standard_genre)
    if len(genres) == 0 or genre_string == '':
       return None
    return ','.join(genres)

df['Genre'] = df['Genre'].apply(extract_genres)
df = df.dropna(subset=['Genre'], how='any', axis=0)

unique_genres = df['Genre'].str.split(r',| and ').explode().str.strip().unique().tolist()
genres_path = 'data/genres.json'
with open(genres_path, 'w') as json_file:
  json.dump(unique_genres, json_file, indent=4)

df.replace({r'[^\x00-\x7F]+':' '}, regex=True, inplace=True)

clean_movies_path = 'data/clean_movies.csv'
df.to_csv(clean_movies_path, index=False)
