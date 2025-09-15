import pytest
import tempfile
import json
from pathlib import Path
from projviz.scanner import ProjectScanner

class TestProjectScanner:
    def setup_method(self):
        """Set up a temporary directory for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def teardown_method(self):
        """Clean up temporary directory"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_scanner_initialization(self):
        """Test scanner initialization"""
        scanner = ProjectScanner(self.temp_dir)
        assert scanner.root_path == self.temp_path
        assert scanner.node_counter == 0
    
    def test_generate_tree_empty_directory(self):
        """Test tree generation for empty directory"""
        scanner = ProjectScanner(self.temp_dir)
        tree, counter = scanner.generate_tree()
        
        assert tree['type'] == 'folder'
        assert tree['value'] == Path(self.temp_dir).name
        assert tree['data'] == []
        assert counter == 1
    
    def test_generate_tree_with_files(self):
        """Test tree generation with files and directories"""
        # Create test files and directories
        (self.temp_path / 'test_file.py').write_text('print("hello")')
        (self.temp_path / 'test_dir').mkdir()
        (self.temp_path / 'test_dir' / 'nested_file.txt').write_text('nested content')
        
        scanner = ProjectScanner(self.temp_dir)
        tree, counter = scanner.generate_tree()
        
        assert tree['type'] == 'folder'
        assert len(tree['data']) == 2  # test_file.py and test_dir
        
        # Check file node
        file_node = next(node for node in tree['data'] if node['type'] == 'file')
        assert file_node['value'] == 'test_file.py'
        assert file_node['path'] == 'test_file.py'
        
        # Check directory node
        dir_node = next(node for node in tree['data'] if node['type'] == 'folder')
        assert dir_node['value'] == 'test_dir'
        assert len(dir_node['data']) == 1  # nested_file.txt
    
    def test_ignore_patterns(self):
        """Test that ignore patterns are respected"""
        # Create files that should be ignored
        (self.temp_path / '.git').mkdir()
        (self.temp_path / '__pycache__').mkdir()
        (self.temp_path / 'normal_file.py').write_text('print("hello")')
        
        scanner = ProjectScanner(self.temp_dir)
        tree, _ = scanner.generate_tree()
        
        # Should only have normal_file.py, not .git or __pycache__
        assert len(tree['data']) == 1
        assert tree['data'][0]['value'] == 'normal_file.py'
    
    def test_detect_framework_django(self):
        """Test Django framework detection"""
        # Create Django-like structure
        (self.temp_path / 'manage.py').write_text('import django')
        (self.temp_path / 'settings.py').write_text('DEBUG = True')
        
        scanner = ProjectScanner(self.temp_dir)
        framework = scanner.detect_framework()
        assert framework == 'django'
    
    def test_detect_framework_flask(self):
        """Test Flask framework detection"""
        # Create Flask-like structure
        (self.temp_path / 'app.py').write_text('from flask import Flask')
        
        scanner = ProjectScanner(self.temp_dir)
        framework = scanner.detect_framework()
        assert framework == 'flask'
    
    def test_detect_framework_fastapi(self):
        """Test FastAPI framework detection"""
        # Create FastAPI-like structure
        (self.temp_path / 'main.py').write_text('from fastapi import FastAPI')
        
        scanner = ProjectScanner(self.temp_dir)
        framework = scanner.detect_framework()
        assert framework == 'fastapi'
    
    def test_detect_framework_by_requirements(self):
        """Test framework detection by requirements.txt"""
        (self.temp_path / 'requirements.txt').write_text('django==4.0.0\nrequests==2.25.0')
        
        scanner = ProjectScanner(self.temp_dir)
        framework = scanner.detect_framework()
        assert framework == 'django'
    
    def test_detect_framework_unknown(self):
        """Test unknown framework detection"""
        (self.temp_path / 'random_file.txt').write_text('some content')
        
        scanner = ProjectScanner(self.temp_dir)
        framework = scanner.detect_framework()
        assert framework == 'unknown'
    
    def test_scan_project(self):
        """Test complete project scanning"""
        # Create a simple project structure
        (self.temp_path / 'app.py').write_text('from flask import Flask')
        (self.temp_path / 'requirements.txt').write_text('flask==2.0.0')
        
        scanner = ProjectScanner(self.temp_dir)
        result = scanner.scan_project()
        
        assert 'metadata' in result
        assert 'tree' in result
        assert result['metadata']['framework'] == 'flask'
        assert result['metadata']['project_name'] == Path(self.temp_dir).name
        assert 'scan_date' in result['metadata']
