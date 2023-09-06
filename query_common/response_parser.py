from qdrant_client.models import ScoredPoint
from typing import List

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

def convert_quadrant_response(response_data : List[ScoredPoint]):
    converted_data = {
        "matches": []
    }
    for res in response_data:
        metadata = {
            "cast": res.payload.get("cast", []),
            "director": res.payload.get("director", []),
            "genre": res.payload.get("genre", []),
            "origin": res.payload.get("origin", ""),
            "year": float(res.payload.get("year", 0))
        }
        id = f"{res.payload.get('title', '')} ({res.payload.get('year', '')})"
        score = res.score

        match = {
            "id": id,
            "metadata": metadata,
            "score": score
        }

        converted_data["matches"].append(match)
    
    return converted_data
