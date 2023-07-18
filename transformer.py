from configuration import model, index

sentences = [
    {
        "id": "1",
        "text": "Inception is a mind-bending science fiction film.",
        "metadata": {"genre": "Science Fiction", "year": 2010}
    },
    {
        "id": "2",
        "text": "The Shawshank Redemption is a highly acclaimed prison drama.",
        "metadata": {"genre": "Drama", "year": 1994}
    },
    {
        "id": "3",
        "text": "Pulp Fiction is a Quentin Tarantino classic filled with crime and dark humor.",
        "metadata": {"genre": "Crime", "year": 1994}
    },
    {
        "id": "4",
        "text": "The Lord of the Rings trilogy is an epic fantasy adventure.",
        "metadata": {"genre": "Fantasy", "year": 2001}
    },
    {
        "id": "5",
        "text": "The Godfather is a gripping mobster drama with brilliant performances.",
        "metadata": {"genre": "Crime", "year": 1972}
    },
    {
        "id": "6",
        "text": "Forrest Gump is a heartwarming tale of an ordinary man's extraordinary life.",
        "metadata": {"genre": "Drama", "year": 1994}
    },
    {
        "id": "7",
        "text": "The Matrix is a groundbreaking sci-fi action film with innovative visual effects.",
        "metadata": {"genre": "Science Fiction", "year": 1999}
    },
    {
        "id": "8",
        "text": "The Dark Knight is a gritty superhero film that redefined the genre.",
        "metadata": {"genre": "Action", "year": 2008}
    },
    {
        "id": "9",
        "text": "Schindler's List is a powerful portrayal of one man's efforts to save lives during the Holocaust.",
        "metadata": {"genre": "Drama", "year": 1993}
    },
    {
        "id": "10",
        "text": "Fight Club is a thought-provoking psychological thriller with an unpredictable storyline.",
        "metadata": {"genre": "Thriller", "year": 1999}
    }
]

embeddings = model.encode([sentence["text"] for sentence in sentences]).tolist()

for i, sentence in enumerate(sentences):
    sentence["embedding"] = embeddings[i]

sentence_tuples = [(s["id"], s["embedding"], s["metadata"]) for s in sentences]

for sentence in sentences:
    index.upsert(vectors=sentence_tuples, batch_size=5)