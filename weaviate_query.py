from weaviate_client import client
import json
from query import create_embedding_from_query

filter = {
    "operator": "And",
    "operands": [
        {
            "path": [
                "genre"
            ],
            "operator": "ContainsAny",
            "valueTextList": [
                "Biographical"
            ]
        },
        {
            "operator": "And",
            "operands": [
                {
                    "path": [
                        "year"
                    ],
                    "operator": "GreaterThan",
                    "valueInt": 1900
                },
                {
                    "path": [
                        "year"
                    ],
                    "operator": "LessThan",
                    "valueInt": 2015
                }
            ]
        },
        {
            "path": [
                "cast"
            ],
            "operator": "ContainsAny",
            "valueTextList": [
                "Florence Lawrence"
            ]
        },
        {
            "path": [
                "origin"
            ],
            "operator": "ContainsAny",
            "valueTextList": [
                "American"
            ]
        },
        {
            "path": [
                "director"
            ],
            "operator": "ContainsAny",
            "valueTextList": [
                "Wallace McCutcheon"
            ]
        }
    ]
}

response = (
    client.query
    .get("Movie", ["title", "year", "genre", "origin", "cast", "director"])
    .with_where(filter)
    .with_near_vector({
        "vector": create_embedding_from_query("Boone's daughter befriends an Indian maiden as Boone and his companion start out on a hunting expedition. While he is away, Boone's cabin is attacked by the Indians, who set it on fire and abduct Boone's daughter.")
    })
    .with_additional(["certainty"])
    .with_limit(3)
    .do()
)

print(json.dumps(response, indent=2))