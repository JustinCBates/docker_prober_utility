#!/usr/bin/env python3
"""
Docker Prober Utility - Flask Backend
Minimal HTTP/HTTPS backend for integration testing and deployment validation
"""

from flask import Flask, jsonify, request
import json
import os
import subprocess
from datetime import datetime

app = Flask(__name__)

PROBE_DATA_FILE = "probe_data.json"


def load_probe_data():
    """Load probe data from JSON file"""
    if os.path.exists(PROBE_DATA_FILE):
        try:
            with open(PROBE_DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Failed to load probe data: {str(e)}"}
    return {"message": "No probe data available yet"}


@app.route('/')
def hello():
    """Simple hello world endpoint"""
    return jsonify({
        "message": "Docker Prober Utility",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/probe')
def probe():
    """Return collected probe data"""
    data = load_probe_data()
    return jsonify(data)


@app.route('/collect', methods=['POST'])
def collect():
    """Trigger host information collection"""
    try:
        # Run the collection script
        result = subprocess.run(
            ['python3', 'scripts/collect_host_info.py', PROBE_DATA_FILE],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return jsonify({
                "status": "success",
                "message": "Host information collected",
                "output": result.stdout
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Collection failed",
                "error": result.stderr
            }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/test')
def test():
    """Test endpoint for proxy and server validation"""
    return jsonify({
        "test": "success",
        "message": "Proxy and server configuration working",
        "client_ip": request.remote_addr,
        "headers": dict(request.headers),
        "timestamp": datetime.now().isoformat()
    })


if __name__ == '__main__':
    # Run on all interfaces, port 8080
    app.run(host='0.0.0.0', port=8080, debug=False)