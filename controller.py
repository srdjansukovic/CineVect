from flask import Flask, request, jsonify
from query import create_embedding_from_query, query_search

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Flask!"

@app.route('/query', methods=['POST'])
def post_example():
    try:
        request_body = request.get_json()

        query = request_body.get('query')
        filter = request_body.get('filter')
        n_results = request_body.get('n_results')

        if not query or not filter or not n_results:
            return jsonify({"error": "Sentence, filter and n_results are required fields."}), 400

        embedding = create_embedding_from_query(query=query)
        pinecone_filter = parse_filter(filter)
        query_response = query_search(embedding=embedding, filter=pinecone_filter, n_results=n_results)

        return query_response.to_dict()

    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500
    
def parse_filter(user_filter):
    return {key: {"$eq": value} for key, value in user_filter.items()}