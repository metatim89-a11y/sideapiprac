import requests

# Airtable CRUD API for Airtable Bridge page
def get_airtable_headers():
    return {
        'Authorization': f"Bearer {os.environ.get('AIRTABLE_TOKEN')}",
        'Content-Type': 'application/json'
    }

BASE_ID = '80913c2e-45b9-4180-a2d2-25b3eb394cae'
TABLE_ID = 'lEwqAOMRR3slxeV/viwJfOGCun29zSDYC'
AIRTABLE_URL = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}'

@app.route('/airtable-data', methods=['GET'])
def airtable_list():
    try:
        resp = requests.get(AIRTABLE_URL, headers=get_airtable_headers())
        return resp.text, resp.status_code, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/airtable-data', methods=['POST'])
def airtable_create():
    try:
        data = request.get_json()
        resp = requests.post(AIRTABLE_URL, headers=get_airtable_headers(), json={"fields": data})
        return resp.text, resp.status_code, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/airtable-data/<record_id>', methods=['PATCH'])
def airtable_update(record_id):
    try:
        data = request.get_json()
        url = f"{AIRTABLE_URL}/{record_id}"
        resp = requests.patch(url, headers=get_airtable_headers(), json={"fields": data})
        return resp.text, resp.status_code, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/airtable-data/<record_id>', methods=['DELETE'])
def airtable_delete(record_id):
    try:
        url = f"{AIRTABLE_URL}/{record_id}"
        resp = requests.delete(url, headers=get_airtable_headers())
        return resp.text, resp.status_code, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500
from flask import Flask, send_from_directory, jsonify, request, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder='docs', template_folder='templates')
@app.route('/api-builder')
def api_builder():
    return render_template('api_builder.html')

@app.route('/webhook-forge')
def webhook_forge():
    return render_template('webhook_forge.html')

@app.route('/data-transformer')
def data_transformer():
    return render_template('data_transformer.html')

@app.route('/airtable-bridge')
def airtable_bridge():
    return render_template('airtable_bridge.html')

@app.route('/learning-hub')
def learning_hub():
    return render_template('learning_hub.html')
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