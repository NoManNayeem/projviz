"""
Framework detection utilities for Project VizTree
"""

import re
from pathlib import Path
from typing import Dict, List, Optional

class FrameworkDetector:
    """Enhanced framework detection with multiple strategies"""
    
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.framework_indicators = {
            'django': {
                'files': ['manage.py', 'wsgi.py', 'asgi.py', 'settings.py'],
                'directories': ['django', 'apps', 'templates', 'static'],
                'imports': ['django', 'django.db', 'django.contrib'],
                'patterns': [r'from django\.', r'import django', r'DJANGO_SETTINGS_MODULE']
            },
            'flask': {
                'files': ['app.py', 'application.py', 'flask_app.py', 'wsgi.py'],
                'directories': ['templates', 'static', 'instance'],
                'imports': ['flask', 'Flask'],
                'patterns': [r'from flask import', r'app = Flask', r'@app\.route']
            },
            'fastapi': {
                'files': ['main.py', 'app.py', 'fastapi_app.py'],
                'directories': ['routers', 'api', 'models'],
                'imports': ['fastapi', 'FastAPI'],
                'patterns': [r'from fastapi import', r'app = FastAPI', r'@app\.get', r'@app\.post']
            },
            'pyramid': {
                'files': ['development.ini', 'production.ini'],
                'directories': ['pyramid'],
                'imports': ['pyramid', 'pyramid.config'],
                'patterns': [r'from pyramid\.', r'config\.make_wsgi_app']
            },
            'tornado': {
                'files': ['main.py', 'app.py'],
                'directories': ['tornado'],
                'imports': ['tornado', 'tornado.web'],
                'patterns': [r'from tornado\.', r'tornado\.web\.Application']
            }
        }
    
    def detect_by_files(self) -> Optional[str]:
        """Detect framework by looking for characteristic files"""
        for framework, indicators in self.framework_indicators.items():
            for file_name in indicators['files']:
                if (self.root_path / file_name).exists():
                    return framework
        return None
    
    def detect_by_directories(self) -> Optional[str]:
        """Detect framework by looking for characteristic directories"""
        for framework, indicators in self.framework_indicators.items():
            for dir_name in indicators['directories']:
                if (self.root_path / dir_name).is_dir():
                    return framework
        return None
    
    def detect_by_dependencies(self) -> Optional[str]:
        """Detect framework by analyzing dependency files"""
        # Check requirements.txt
        requirements_file = self.root_path / 'requirements.txt'
        if requirements_file.exists():
            content = requirements_file.read_text().lower()
            for framework in self.framework_indicators.keys():
                if framework in content:
                    return framework
        
        # Check pyproject.toml
        pyproject_file = self.root_path / 'pyproject.toml'
        if pyproject_file.exists():
            content = pyproject_file.read_text().lower()
            for framework in self.framework_indicators.keys():
                if framework in content:
                    return framework
        
        # Check setup.py
        setup_file = self.root_path / 'setup.py'
        if setup_file.exists():
            content = setup_file.read_text().lower()
            for framework in self.framework_indicators.keys():
                if framework in content:
                    return framework
        
        return None
    
    def detect_by_code_analysis(self) -> Optional[str]:
        """Detect framework by analyzing Python code files"""
        python_files = list(self.root_path.rglob('*.py'))
        
        for framework, indicators in self.framework_indicators.items():
            for pattern in indicators['patterns']:
                regex = re.compile(pattern, re.IGNORECASE)
                for py_file in python_files[:10]:  # Limit to first 10 files for performance
                    try:
                        content = py_file.read_text()
                        if regex.search(content):
                            return framework
                    except (UnicodeDecodeError, PermissionError):
                        continue
        
        return None
    
    def detect_framework(self) -> str:
        """Main detection method using multiple strategies"""
        # Try different detection methods in order of reliability
        methods = [
            self.detect_by_files,
            self.detect_by_directories,
            self.detect_by_dependencies,
            self.detect_by_code_analysis
        ]
        
        for method in methods:
            result = method()
            if result:
                return result
        
        return 'unknown'
    
    def get_framework_info(self, framework: str) -> Dict[str, str]:
        """Get additional information about the detected framework"""
        framework_info = {
            'django': {
                'name': 'Django',
                'description': 'High-level Python web framework',
                'website': 'https://djangoproject.com/',
                'color': '#092e20'
            },
            'flask': {
                'name': 'Flask',
                'description': 'Lightweight WSGI web application framework',
                'website': 'https://flask.palletsprojects.com/',
                'color': '#000000'
            },
            'fastapi': {
                'name': 'FastAPI',
                'description': 'Modern, fast web framework for building APIs',
                'website': 'https://fastapi.tiangolo.com/',
                'color': '#009688'
            },
            'pyramid': {
                'name': 'Pyramid',
                'description': 'Minimalist Python web framework',
                'website': 'https://trypyramid.com/',
                'color': '#8B4513'
            },
            'tornado': {
                'name': 'Tornado',
                'description': 'Python web framework and networking library',
                'website': 'https://www.tornadoweb.org/',
                'color': '#FF6B35'
            },
            'unknown': {
                'name': 'Unknown',
                'description': 'No recognizable framework detected',
                'website': '',
                'color': '#6c757d'
            }
        }
        
        return framework_info.get(framework, framework_info['unknown'])
