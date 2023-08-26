from flask import Flask, request, jsonify
from flask_cors import CORS
from query import create_embedding_from_query, pinecone_query, weaviate_query
from query_parser import convert_to_pinecone_syntax, convert_to_weaviate_syntax
from response_parser import convert_weaviate_response

app = Flask(__name__)
CORS(app)

@app.route('/query/pinecone', methods=['POST'])
def pinecone_search():
    try:
        request_body = request.get_json()

        query = request_body.get('queryText')
        n_results = 4

        if not query:
            return jsonify({"error": "Query text is required."}), 400

        embedding = create_embedding_from_query(query=query)
        pinecone_filter = convert_to_pinecone_syntax(request_body)
        query_response = pinecone_query(embedding=embedding, filter=pinecone_filter, n_results=n_results)

        return query_response.to_dict()

    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500
    
@app.route('/query/weaviate', methods=['POST'])
def weaviate_search():
    try:
        request_body = request.get_json()

        query = request_body.get('queryText')
        n_results = 4

        if not query:
            return jsonify({"error": "Query text is required."}), 400

        embedding = create_embedding_from_query(query=query)
        weaviate_filter = convert_to_weaviate_syntax(request_body)
        query_response = weaviate_query(embedding=embedding, filter=weaviate_filter, n_results=n_results)

        return convert_weaviate_response(query_response)

    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500
    