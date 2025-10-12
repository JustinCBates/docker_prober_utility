import unittest
import json
import os
import sys
from pathlib import Path
from io import StringIO
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

import view_probe_data


class TestViewProbeData(unittest.TestCase):
    """Test cases for the probe data viewer script"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_data_file = "test_probe_view.json"
        self.test_data = {
            "timestamp": "2025-10-11T12:00:00",
            "network": {
                "hostname": "test-host",
                "fqdn": "test-host.example.com",
                "ip_addresses": ["192.168.1.100", "10.0.0.1"]
            },
            "resources": {
                "cpu_count": 4,
                "cpu_info": "Intel Core i5",
                "load_average": [0.5, 0.7, 0.9]
            },
            "os_details": {
                "system": "Linux",
                "release": "5.10.0",
                "machine": "x86_64",
                "kernel_version": "5.10.0-23"
            },
            "docker_environment": {
                "docker_version": "Docker version 24.0.0",
                "docker_compose_version": "docker-compose version 1.29.2",
                "docker_status": "active"
            },
            "environment_variables": {
                "PATH": "/usr/bin:/bin",
                "HOME": "/root",
                "USER": "root"
            },
            "storage": {
                "available_space": "50G available"
            },
            "proxy_dns": {},
            "locale": {}
        }
        
        # Save test data
        with open(self.test_data_file, 'w') as f:
            json.dump(self.test_data, f)
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
    
    def test_load_probe_data_success(self):
        """Test loading valid probe data"""
        data = view_probe_data.load_probe_data(self.test_data_file)
        self.assertEqual(data['timestamp'], '2025-10-11T12:00:00')
        self.assertEqual(data['network']['hostname'], 'test-host')
    
    def test_load_probe_data_missing_file(self):
        """Test loading non-existent file"""
        with self.assertRaises(SystemExit):
            view_probe_data.load_probe_data('nonexistent.json')
    
    def test_load_probe_data_invalid_json(self):
        """Test loading invalid JSON file"""
        invalid_file = "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write("not valid json {[")
        
        try:
            with self.assertRaises(SystemExit):
                view_probe_data.load_probe_data(invalid_file)
        finally:
            os.remove(invalid_file)
    
    def test_display_probe_data_plain(self):
        """Test plain text display output"""
        output = StringIO()
        
        with patch('sys.stdout', output):
            view_probe_data.display_probe_data_plain(self.test_data)
        
        result = output.getvalue()
        
        # Check that key information is displayed
        self.assertIn('test-host', result)
        self.assertIn('192.168.1.100', result)
        self.assertIn('Linux', result)
        self.assertIn('CPU Count: 4', result)
        self.assertIn('Docker version 24.0.0', result)
    
    @patch('view_probe_data.RICH_AVAILABLE', False)
    def test_display_without_rich(self):
        """Test display falls back to plain when rich not available"""
        output = StringIO()
        
        with patch('sys.stdout', output):
            view_probe_data.display_probe_data_plain(self.test_data)
        
        result = output.getvalue()
        self.assertIn('test-host', result)
    
    def test_create_network_table(self):
        """Test network table creation (if rich is available)"""
        if view_probe_data.RICH_AVAILABLE:
            table = view_probe_data.create_network_table(self.test_data['network'])
            self.assertIsNotNone(table)
    
    def test_create_resources_table(self):
        """Test resources table creation (if rich is available)"""
        if view_probe_data.RICH_AVAILABLE:
            table = view_probe_data.create_resources_table(self.test_data['resources'])
            self.assertIsNotNone(table)
    
    def test_create_os_table(self):
        """Test OS table creation (if rich is available)"""
        if view_probe_data.RICH_AVAILABLE:
            table = view_probe_data.create_os_table(self.test_data['os_details'])
            self.assertIsNotNone(table)
    
    def test_create_docker_table(self):
        """Test Docker table creation (if rich is available)"""
        if view_probe_data.RICH_AVAILABLE:
            table = view_probe_data.create_docker_table(self.test_data['docker_environment'])
            self.assertIsNotNone(table)
    
    def test_main_with_default_file(self):
        """Test main function with default filename"""
        # Create probe_data.json for default test
        with open('probe_data.json', 'w') as f:
            json.dump(self.test_data, f)
        
        try:
            output = StringIO()
            with patch('sys.stdout', output):
                with patch('sys.argv', ['view_probe_data.py']):
                    # Should not raise exception
                    pass
        finally:
            if os.path.exists('probe_data.json'):
                os.remove('probe_data.json')
    
    def test_main_with_custom_file(self):
        """Test main function with custom filename argument"""
        output = StringIO()
        with patch('sys.stdout', output):
            with patch('sys.argv', ['view_probe_data.py', self.test_data_file]):
                # Should not raise exception
                data = view_probe_data.load_probe_data(self.test_data_file)
                self.assertIsNotNone(data)


if __name__ == '__main__':
    unittest.main()
