from qdrant_db.qdrant_client import qdrant
from qdrant_client import models
from query_common.query import create_embedding_from_query

embedding = create_embedding_from_query("In 1947 Portland, Maine, banker Andy Dufresne is convicted of murdering his wife and her lover, and sentenced to two consecutive life sentences at the Shawshank State Penitentiary. He is befriended by contraband smuggler, Ellis 'Red' Redding, an inmate serving a life sentence.")

filter = models.Filter(
  must=[
    models.FieldCondition(
      key="genre",
      match=models.MatchAny(any=["Drama"])
    ),
    models.FieldCondition(
      key="year",
      range=models.Range(
        gte=1900,
        lte=2015
      )
    ),
    models.FieldCondition(
      key="origin",
      match=models.MatchValue(value="American"),
    ),
    models.FieldCondition(
      key="cast",
      match=models.MatchAny(any=["Tim Robbins", "Morgan Freeman"])
    ),
    models.FieldCondition(
      key="director",
      match=models.MatchAny(any=["Frank Darabont"])
    ),
  ]
)

res = qdrant.search(
    collection_name="movies",
    query_vector=embedding,
    with_payload=True,
    query_filter=filter,
    limit=4
)

for r in res:
  print(r.payload.get("cast"))

print(res)