"""
Simple test script to check if Flask server works
"""
from flask import Flask, jsonify
from flask_cors import CORS
import sys
import traceback

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Test Flask server is running'
    })

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({
        'test': 'success',
        'data': [1, 2, 3, 4, 5]
    })

if __name__ == '__main__':
    try:
        print("🚀 Starting test Flask server...")
        print("📡 Server will run on: http://localhost:5000")
        print("🔗 Test endpoint: http://localhost:5000/api/health")
        print("🛑 Press Ctrl+C to stop")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        traceback.print_exc()
        sys.exit(1)
