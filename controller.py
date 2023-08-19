from flask import Flask, request, jsonify
from flask_cors import CORS
from query import create_embedding_from_query, query_search
import json

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['POST'])
def post_example():
    try:
        request_body = request.get_json()

        query = request_body.get('queryText')
        n_results = 4

        if not query:
            return jsonify({"error": "Query text is required."}), 400

        embedding = create_embedding_from_query(query=query)
        pinecone_filter = parse_filter(request_body)
        query_response = query_search(embedding=embedding, filter=pinecone_filter, n_results=n_results)

        return query_response.to_dict()

    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500
    
def parse_filter(user_filter):
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