import unittest
import json
import os
import sys
from pathlib import Path

# Add parent directory to path to import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app


class ProberTestCase(unittest.TestCase):
    """Test cases for the Flask application endpoints"""
    
    def setUp(self):
        """Set up test client and testing mode"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Create a test probe data file
        self.test_probe_data = {
            "timestamp": "2025-10-11T12:00:00",
            "network": {
                "hostname": "test-host",
                "ip_addresses": ["192.168.1.100"]
            },
            "resources": {
                "cpu_count": 4
            }
        }
        
        # Save test data
        with open('probe_data.json', 'w') as f:
            json.dump(self.test_probe_data, f)
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists('probe_data.json'):
            os.remove('probe_data.json')
    
    def test_root_endpoint(self):
        """Test the root / endpoint returns proper JSON"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('status', data)
        self.assertEqual(data['message'], 'Docker Prober Utility')
        self.assertEqual(data['status'], 'running')
    
    def test_health_endpoint(self):
        """Test the /health endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
    
    def test_probe_endpoint(self):
        """Test the /probe endpoint returns probe data"""
        response = self.app.get('/probe')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('timestamp', data)
        self.assertIn('network', data)
        self.assertEqual(data['network']['hostname'], 'test-host')
    
    def test_probe_endpoint_no_data(self):
        """Test /probe endpoint when no data file exists"""
        os.remove('probe_data.json')
        response = self.app.get('/probe')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
    
    def test_test_endpoint(self):
        """Test the /test endpoint for proxy validation"""
        response = self.app.get('/test')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['test'], 'success')
        self.assertIn('client_ip', data)
        self.assertIn('headers', data)
        self.assertIn('timestamp', data)
    
    def test_collect_endpoint_post(self):
        """Test the /collect POST endpoint"""
        response = self.app.post('/collect')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
    
    def test_invalid_endpoint(self):
        """Test that invalid endpoints return 404"""
        response = self.app.get('/invalid')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
