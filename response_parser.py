
def convert_weaviate_response(response_data):
    converted_data = {
        "matches": []
    }

    movies = response_data.get("data", {}).get("Get", {}).get("Movie", [])
    for movie in movies:
        metadata = {
            "cast": movie.get("cast", []),
            "director": movie.get("director", []),
            "genre": movie.get("genre", []),
            "origin": movie.get("origin", ""),
            "year": float(movie.get("year", 0))
        }
        id = f"{movie.get('title', '')} ({movie.get('year', '')})"
        score = movie.get("_additional", {}).get("certainty", 0.0)

        match = {
            "id": id,
            "metadata": metadata,
            "score": score
        }

        converted_data["matches"].append(match)

    return converted_data