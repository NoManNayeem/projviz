import pytest
import tempfile
from pathlib import Path
from projviz.framework_detection import FrameworkDetector

class TestFrameworkDetection:
    def setup_method(self):
        """Set up a temporary directory for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def teardown_method(self):
        """Clean up temporary directory"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_detector_initialization(self):
        """Test framework detector initialization"""
        detector = FrameworkDetector(self.temp_path)
        assert detector.root_path == self.temp_path
        assert 'django' in detector.framework_indicators
        assert 'flask' in detector.framework_indicators
        assert 'fastapi' in detector.framework_indicators
    
    def test_detect_by_files_django(self):
        """Test Django detection by files"""
        (self.temp_path / 'manage.py').write_text('import django')
        detector = FrameworkDetector(self.temp_path)
        result = detector.detect_by_files()
        assert result == 'django'
    
    def test_detect_by_files_flask(self):
        """Test Flask detection by files"""
        (self.temp_path / 'app.py').write_text('from flask import Flask')
        detector = FrameworkDetector(self.temp_path)
        result = detector.detect_by_files()
        assert result == 'flask'
    
    def test_detect_by_files_fastapi(self):
        """Test FastAPI detection by files"""
        (self.temp_path / 'main.py').write_text('from fastapi import FastAPI')
        detector = FrameworkDetector(self.temp_path)
        result = detector.detect_by_files()
        assert result == 'fastapi'
    
    def test_detect_by_directories_django(self):
        """Test Django detection by directories"""
        (self.temp_path / 'django').mkdir()
        detector = FrameworkDetector(self.temp_path)
        result = detector.detect_by_directories()
        assert result == 'django'
    
    def test_detect_by_directories_flask(self):
        """Test Flask detection by directories"""
        (self.temp_path / 'templates').mkdir()
        detector = FrameworkDetector(self.temp_path)
        result = detector.detect_by_directories()
        assert result == 'flask'
    
    def test_detect_by_dependencies_requirements(self):
        """Test framework detection by requirements.txt"""
        (self.temp_path / 'requirements.txt').write_text('django==4.0.0\nrequests==2.25.0')
        detector = FrameworkDetector(self.temp_path)
        result = detector.detect_by_dependencies()
        assert result == 'django'
    
    def test_detect_by_dependencies_pyproject(self):
        """Test framework detection by pyproject.toml"""
        (self.temp_path / 'pyproject.toml').write_text('[project]\ndependencies = ["fastapi>=0.68.0"]')
        detector = FrameworkDetector(self.temp_path)
        result = detector.detect_by_dependencies()
        assert result == 'fastapi'
    
    def test_detect_by_code_analysis_flask(self):
        """Test Flask detection by code analysis"""
        (self.temp_path / 'myapp.py').write_text('from flask import Flask\napp = Flask(__name__)')
        detector = FrameworkDetector(self.temp_path)
        result = detector.detect_by_code_analysis()
        assert result == 'flask'
    
    def test_detect_by_code_analysis_fastapi(self):
        """Test FastAPI detection by code analysis"""
        (self.temp_path / 'api.py').write_text('from fastapi import FastAPI\napp = FastAPI()')
        detector = FrameworkDetector(self.temp_path)
        result = detector.detect_by_code_analysis()
        assert result == 'fastapi'
    
    def test_detect_framework_priority(self):
        """Test that file detection takes priority over other methods"""
        # Create both file and requirements.txt
        (self.temp_path / 'manage.py').write_text('import django')
        (self.temp_path / 'requirements.txt').write_text('flask==2.0.0')
        
        detector = FrameworkDetector(self.temp_path)
        result = detector.detect_framework()
        assert result == 'django'  # File detection should take priority
    
    def test_detect_framework_unknown(self):
        """Test unknown framework detection"""
        (self.temp_path / 'random_file.txt').write_text('some content')
        detector = FrameworkDetector(self.temp_path)
        result = detector.detect_framework()
        assert result == 'unknown'
    
    def test_get_framework_info_django(self):
        """Test getting Django framework info"""
        detector = FrameworkDetector(self.temp_path)
        info = detector.get_framework_info('django')
        assert info['name'] == 'Django'
        assert 'web framework' in info['description']
        assert 'djangoproject.com' in info['website']
    
    def test_get_framework_info_flask(self):
        """Test getting Flask framework info"""
        detector = FrameworkDetector(self.temp_path)
        info = detector.get_framework_info('flask')
        assert info['name'] == 'Flask'
        assert 'WSGI' in info['description']
        assert 'flask.palletsprojects.com' in info['website']
    
    def test_get_framework_info_unknown(self):
        """Test getting unknown framework info"""
        detector = FrameworkDetector(self.temp_path)
        info = detector.get_framework_info('unknown')
        assert info['name'] == 'Unknown'
        assert 'No recognizable framework' in info['description']
