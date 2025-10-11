import unittest
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from collect_host_info import collect_host_info, save_to_json, run_command


class TestCollectHostInfo(unittest.TestCase):
    """Test cases for host information collection script"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_output_file = "test_probe_data.json"
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_output_file):
            os.remove(self.test_output_file)
    
    def test_run_command_success(self):
        """Test run_command with successful command"""
        result = run_command("echo 'test'")
        self.assertEqual(result, "test")
    
    def test_run_command_failure(self):
        """Test run_command with failing command"""
        result = run_command("false")
        self.assertIsNone(result)
    
    def test_collect_host_info_structure(self):
        """Test that collect_host_info returns proper structure"""
        info = collect_host_info()
        
        # Check all required keys exist
        required_keys = [
            'timestamp', 'network', 'resources', 'os_details',
            'docker_environment', 'environment_variables',
            'storage', 'proxy_dns', 'locale'
        ]
        
        for key in required_keys:
            self.assertIn(key, info)
    
    def test_collect_host_info_network(self):
        """Test network information collection"""
        info = collect_host_info()
        network = info['network']
        
        self.assertIn('hostname', network)
        self.assertIn('fqdn', network)
        self.assertIn('ip_addresses', network)
        
        # Hostname should not be empty
        self.assertTrue(network['hostname'])
    
    def test_collect_host_info_resources(self):
        """Test resource information collection"""
        info = collect_host_info()
        resources = info['resources']
        
        self.assertIn('cpu_count', resources)
        self.assertIn('memory_info', resources)
        self.assertIn('disk_usage', resources)
        
        # CPU count should be a positive integer
        self.assertIsInstance(resources['cpu_count'], int)
        self.assertGreater(resources['cpu_count'], 0)
    
    def test_collect_host_info_os_details(self):
        """Test OS details collection"""
        info = collect_host_info()
        os_details = info['os_details']
        
        self.assertIn('system', os_details)
        self.assertIn('release', os_details)
        self.assertIn('machine', os_details)
        
        # System should not be empty
        self.assertTrue(os_details['system'])
    
    def test_collect_host_info_environment_variables(self):
        """Test environment variables collection"""
        info = collect_host_info()
        env_vars = info['environment_variables']
        
        # Should have at least some environment variables
        self.assertGreater(len(env_vars), 0)
        
        # Should include PATH
        self.assertIn('PATH', env_vars)
    
    def test_save_to_json_success(self):
        """Test successful JSON save"""
        test_data = {
            "test": "data",
            "timestamp": "2025-10-11T12:00:00"
        }
        
        result = save_to_json(test_data, self.test_output_file)
        self.assertTrue(result)
        
        # Verify file exists and contains correct data
        self.assertTrue(os.path.exists(self.test_output_file))
        
        with open(self.test_output_file, 'r') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data['test'], 'data')
    
    def test_save_to_json_invalid_path(self):
        """Test save_to_json with invalid path"""
        test_data = {"test": "data"}
        result = save_to_json(test_data, "/invalid/path/file.json")
        self.assertFalse(result)
    
    @patch('collect_host_info.run_command')
    def test_collect_with_mocked_commands(self, mock_run):
        """Test collection with mocked system commands"""
        mock_run.return_value = "mocked output"
        
        info = collect_host_info()
        
        # Should still have structure even with mocked commands
        self.assertIn('network', info)
        self.assertIn('resources', info)
        self.assertIn('os_details', info)


if __name__ == '__main__':
    unittest.main()
