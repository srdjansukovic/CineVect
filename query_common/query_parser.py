import json
from qdrant_client import models

def convert_to_pinecone_syntax(user_filter):
    pinecone_filter = {}

    if user_filter.get("genres"):
        pinecone_filter["genre"] = {"$in": user_filter["genres"]}

    if user_filter.get("minYear") and user_filter.get("maxYear"):
        year_range = {}
        if user_filter.get("minYear"):
            year_range["$gte"] = int(user_filter["minYear"])
        if user_filter.get("maxYear"):
            year_range["$lte"] = int(user_filter["maxYear"])
        pinecone_filter["year"] = year_range

    if user_filter.get("actors"):
        pinecone_filter["cast"] = {"$in": user_filter["actors"]}

    if user_filter.get("origins"):
        pinecone_filter["origin"] = {"$in": user_filter["origins"]}

    if user_filter.get("directors"):
        pinecone_filter["director"] = {"$in": user_filter["directors"]}

    print('Created pinecone filter: ', json.dumps(pinecone_filter, indent=2))
    return pinecone_filter

def convert_to_weaviate_syntax(request_body):
    weaviate_syntax = {
        "operator": "And",
        "operands": []
    }

    if request_body.get("genres"):
        genre_filter = {
            "path": ["genre"],
            "operator": "ContainsAny",
            "valueTextList": request_body.get("genres")
        }
        weaviate_syntax["operands"].append(genre_filter)

    if "minYear" in request_body and request_body.get("minYear"):
        if "maxYear" in request_body and request_body.get("maxYear"):
            year_filter = {
                "operator": "And",
                "operands": [
                    {
                        "path": ["year"],
                        "operator": "GreaterThan",
                        "valueInt": int(request_body.get("minYear"))
                    },
                    {
                        "path": ["year"],
                        "operator": "LessThan",
                        "valueInt": int(request_body.get("maxYear"))
                    }
                ]
            }
            weaviate_syntax["operands"].append(year_filter)
        else:
            year_filter = {
                "path": ["year"],
                "operator": "GreaterThan",
                "valueInt": int(request_body.get("minYear"))
            }
            weaviate_syntax["operands"].append(year_filter)

    if "actors" in request_body and request_body.get("actors"):
        actors_filter = {
            "path": ["cast"],
            "operator": "ContainsAny",
            "valueTextList": request_body.get("actors")
        }
        weaviate_syntax["operands"].append(actors_filter)

    if "origins" in request_body and request_body.get("origins"):
        origin_filter = {
            "path": ["origin"],
            "operator": "ContainsAny",
            "valueTextList": request_body.get("origins")
        }
        weaviate_syntax["operands"].append(origin_filter)

    if "directors" in request_body and request_body.get("directors"):
        directors_filter = {
            "path": ["director"],
            "operator": "ContainsAny",
            "valueTextList": request_body.get("directors")
        }
        weaviate_syntax["operands"].append(directors_filter)
    
    print('Created weaviate filter: ', json.dumps(weaviate_syntax, indent=2))

    return weaviate_syntax

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
                gte=user_filter.get("minYear"),
                lte=user_filter.get("maxYear")
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

