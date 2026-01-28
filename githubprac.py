from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='docs', template_folder='docs')
CORS(app)

@app.route('/')
def home():
    # Serve the landing page from docs/
    return send_from_directory('docs', 'index.html')

@app.route('/api/v1/entries', methods=['GET'])
def entries():
    """Mock entries endpoint for experimentation.

    Query params:
      - page: integer (default 1)
      - size: integer (default 10)
    """
    try:
        page = int(request.args.get('page', 1))
    except (ValueError, TypeError):
        page = 1
    try:
        size = int(request.args.get('size', 10))
    except (ValueError, TypeError):
        size = 10

    # Keep size within reasonable bounds in the mock
    size = max(1, min(size, 100))

    start = (page - 1) * size + 1
    items = []
    for i in range(start, start + size):
        items.append({
            'id': i,
            'title': f'Example entry {i}',
            'summary': 'A safe sandbox response.'
        })

    payload = {
        'page': page,
        'size': size,
        'items': items
    }
    return jsonify(payload)

if __name__ == '__main__':
    # Allow the port to be configurable via PORT env var for easy deployment
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)