import json
from qdrant_client import models
import datetime

current_year = datetime.datetime.now().year
minimum_year = 1800

def convert_to_pinecone_syntax(user_filter):
    pinecone_filter = {}

    if user_filter.get("genres"):
        pinecone_filter["genre"] = {"$in": user_filter["genres"]}

    if user_filter.get("minYear") or user_filter.get("maxYear"):
        year_range = {}
        year_range["$gte"] = int(user_filter["minYear"] or minimum_year)
        year_range["$lte"] = int(user_filter["maxYear"] or current_year)
        pinecone_filter["year"] = year_range

    if user_filter.get("actors"):
        pinecone_filter["cast"] = {"$in": user_filter["actors"]}

    if user_filter.get("origins"):
        pinecone_filter["origin"] = {"$in": user_filter["origins"]}

    if user_filter.get("directors"):
        pinecone_filter["director"] = {"$in": user_filter["directors"]}

    print('Created pinecone filter: ', json.dumps(pinecone_filter, indent=2))
    return pinecone_filter

def convert_to_weaviate_syntax(user_filter):
    weaviate_filter = {
        "operator": "And",
        "operands": []
    }

    if user_filter.get("genres"):
        genre_filter = {
            "path": ["genre"],
            "operator": "ContainsAny",
            "valueTextList": user_filter.get("genres")
        }
        weaviate_filter["operands"].append(genre_filter)
    
    if user_filter.get("minYear") or user_filter.get("maxYear"):
        year_filter = {
            "operator": "And",
            "operands": [
                {
                    "path": ["year"],
                    "operator": "GreaterThanEqual",
                    "valueInt": int(user_filter.get("minYear") or minimum_year)
                },
                {
                    "path": ["year"],
                    "operator": "LessThanEqual",
                    "valueInt": int(user_filter.get("maxYear") or current_year)
                }
            ]
        }
        weaviate_filter["operands"].append(year_filter)

    if "actors" in user_filter and user_filter.get("actors"):
        actors_filter = {
            "path": ["cast"],
            "operator": "ContainsAny",
            "valueTextList": user_filter.get("actors")
        }
        weaviate_filter["operands"].append(actors_filter)

    if "origins" in user_filter and user_filter.get("origins"):
        origin_filter = {
            "path": ["origin"],
            "operator": "ContainsAny",
            "valueTextList": user_filter.get("origins")
        }
        weaviate_filter["operands"].append(origin_filter)

    if "directors" in user_filter and user_filter.get("directors"):
        directors_filter = {
            "path": ["director"],
            "operator": "ContainsAny",
            "valueTextList": user_filter.get("directors")
        }
        weaviate_filter["operands"].append(directors_filter)
    
    print('Created weaviate filter: ', json.dumps(weaviate_filter, indent=2))

    return weaviate_filter

def convert_to_qdrant_syntax(user_filter):
    must = []
    if user_filter.get("genres"):
        must.append(models.FieldCondition(
            key="genre",
            match=models.MatchAny(any=user_filter["genres"])
        ))
    if user_filter.get("minYear") or user_filter.get("maxYear"):
        must.append(models.FieldCondition(
            key="year",
            range=models.Range(
                gte=user_filter.get("minYear") or minimum_year,
                lte=user_filter.get("maxYear") or current_year
            )
        ))
    if user_filter.get("actors"):
        must.append(models.FieldCondition(
            key="cast",
            match=models.MatchAny(any=user_filter["actors"])
        ))
    if user_filter.get("origins"):
        must.append(models.FieldCondition(
            key="origin",
            match=models.MatchAny(any=user_filter["origins"])
        ))
    if user_filter.get("directors"):
        must.append(models.FieldCondition(
            key="director",
            match=models.MatchAny(any=user_filter["directors"])
        ))
    
    qdrant_filter = models.Filter(
        must=must
    )

    return qdrant_filter

