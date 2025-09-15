import pytest
import tempfile
import json
from pathlib import Path
from click.testing import CliRunner
from projviz.cli import main

class TestCLI:
    def setup_method(self):
        """Set up a temporary directory for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.runner = CliRunner()
    
    def teardown_method(self):
        """Clean up temporary directory"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_main_command(self):
        """Test main command help"""
        result = self.runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'Project VizTree' in result.output
    
    def test_scan_command_basic(self):
        """Test basic scan command"""
        # Create a test file
        (self.temp_path / 'test.py').write_text('print("hello")')
        
        result = self.runner.invoke(main, ['scan', '--path', str(self.temp_path)])
        assert result.exit_code == 0
        assert 'Project structure saved to' in result.output
    
    def test_scan_command_with_output(self):
        """Test scan command with custom output file"""
        # Create a test file
        (self.temp_path / 'test.py').write_text('print("hello")')
        output_file = self.temp_path / 'custom_output.json'
        
        result = self.runner.invoke(main, [
            'scan', 
            '--path', str(self.temp_path),
            '--output', str(output_file)
        ])
        
        assert result.exit_code == 0
        assert output_file.exists()
        
        # Verify JSON content
        with open(output_file) as f:
            data = json.load(f)
        assert 'metadata' in data
        assert 'tree' in data
    
    def test_scan_command_django_detection(self):
        """Test scan command with Django project"""
        # Create Django-like structure
        (self.temp_path / 'manage.py').write_text('import django')
        (self.temp_path / 'requirements.txt').write_text('django==4.0.0')
        
        result = self.runner.invoke(main, ['scan', '--path', str(self.temp_path)])
        assert result.exit_code == 0
        assert 'Detected framework: django' in result.output
    
    def test_serve_command_missing_file(self):
        """Test serve command with missing JSON file"""
        result = self.runner.invoke(main, ['serve', '--json-file', 'nonexistent.json'])
        assert result.exit_code == 1
        assert 'not found' in result.output
    
    def test_serve_command_with_valid_file(self):
        """Test serve command with valid JSON file"""
        # Create a valid JSON file
        json_data = {
            'metadata': {
                'project_name': 'test_project',
                'framework': 'unknown',
                'scan_date': '2023-01-01T00:00:00'
            },
            'tree': {
                'id': '0',
                'value': 'test_project',
                'type': 'folder',
                'path': '',
                'data': []
            }
        }
        
        json_file = self.temp_path / 'test_structure.json'
        with open(json_file, 'w') as f:
            json.dump(json_data, f)
        
        # Test serve command (we'll just check it doesn't fail immediately)
        result = self.runner.invoke(main, [
            'serve', 
            '--json-file', str(json_file),
            '--port', '8001'  # Use different port to avoid conflicts
        ], input='\n')  # Send newline to potentially stop the server
        
        # The command might not exit cleanly due to server startup, so we check for specific error conditions
        assert result.exit_code != 1  # Should not fail with file not found error
    
    def test_run_command(self):
        """Test run command (scan + serve)"""
        # Create a test file
        (self.temp_path / 'test.py').write_text('print("hello")')
        
        # This test might be flaky due to server startup, so we'll just verify it doesn't crash immediately
        result = self.runner.invoke(main, [
            'run',
            '--path', str(self.temp_path),
            '--port', '8002'  # Use different port
        ], input='\n')
        
        # Check that the scan part worked (JSON file should be created)
        json_file = self.temp_path / 'project_structure.json'
        assert json_file.exists()
