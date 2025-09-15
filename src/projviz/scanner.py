import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any, Callable, Optional
from datetime import datetime

class ProjectScanner:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.node_counter = 0
        self.ignore_patterns = ['.git', '__pycache__', '.venv', 'node_modules', '.pytest_cache', '.mypy_cache']
        # Windows reserved device names that can appear and confuse scanning/rendering
        self._win_reserved = {
            'CON','PRN','AUX','NUL',
            'COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9',
            'LPT1','LPT2','LPT3','LPT4','LPT5','LPT6','LPT7','LPT8','LPT9'
        }

    def _is_reserved_windows_name(self, name: str) -> bool:
        if os.name != 'nt':
            return False
        # Compare without extension and case-insensitive
        stem = name.split('.')[0].upper()
        return stem in self._win_reserved

    def _is_ignored(self, path: Path) -> bool:
        name = path.name
        if self._is_reserved_windows_name(name):
            return True
        # Simple substring-based ignore for common folders/files
        for pattern in self.ignore_patterns:
            if pattern in name:
                return True
        return False
        
    def generate_tree(self, path: Optional[Path] = None, parent_path: str = "", *, printer: Optional[Callable[[str, str, int], None]] = None, depth: int = 0) -> Tuple[Dict, int]:
        if path is None:
            path = self.root_path
            
        name = path.name
        # Normalize to POSIX-style paths for consistency across OSes
        relative_path = path.relative_to(self.root_path).as_posix() if path != self.root_path else ""
        node_id = str(self.node_counter)
        self.node_counter += 1
        
        if path.is_dir():
            # For root directory, use project name, otherwise use directory name
            if path == self.root_path:
                display_name = self.root_path.resolve().name
            else:
                display_name = name
            # Print folder when encountered
            if callable(printer):
                # Show project name for root, else relative path
                to_print = display_name if relative_path == "" else relative_path
                printer('folder', to_print, depth)
            node = {
                "id": node_id,
                "value": display_name,
                "type": "folder",
                "path": relative_path,
                "open": True,  # Open folders by default for better visibility
                "data": []
            }
            
            try:
                # Deterministic ordering: folders first, then files; alphabetical
                items = sorted(
                    [p for p in path.iterdir() if not self._is_ignored(p) and not p.is_symlink()],
                    key=lambda p: (p.is_file(), p.name.lower())
                )
                for item in items:
                    child_node = self.generate_tree(item, relative_path, printer=printer, depth=depth+1)
                    node["data"].append(child_node[0])
            except PermissionError:
                node["value"] = f"{name} (Permission Denied)"
                
            return node, self.node_counter
        else:
            # Print file when encountered
            if callable(printer):
                to_print = relative_path if relative_path else name
                printer('file', to_print, depth)
            return {
                "id": node_id,
                "value": name,
                "type": "file",
                "path": relative_path
            }, self.node_counter
    
    def detect_framework(self) -> str:
        """Detect the Python web framework being used"""
        framework_indicators = {
            'django': ['manage.py', 'wsgi.py', 'asgi.py'],
            'flask': ['app.py', 'application.py', 'flask_app.py'],
            'fastapi': ['main.py', 'app.py', 'fastapi_app.py']
        }
        
        for file in self.root_path.iterdir():
            for framework, indicators in framework_indicators.items():
                if file.name in indicators:
                    return framework
        
        # Check for requirements.txt or pyproject.toml dependencies
        requirements_file = self.root_path / 'requirements.txt'
        if requirements_file.exists():
            with open(requirements_file, 'r') as f:
                content = f.read().lower()
                if 'django' in content:
                    return 'django'
                elif 'flask' in content:
                    return 'flask'
                elif 'fastapi' in content:
                    return 'fastapi'
        
        # Check pyproject.toml
        pyproject_file = self.root_path / 'pyproject.toml'
        if pyproject_file.exists():
            with open(pyproject_file, 'r') as f:
                content = f.read().lower()
                if 'django' in content:
                    return 'django'
                elif 'flask' in content:
                    return 'flask'
                elif 'fastapi' in content:
                    return 'fastapi'
        
        return 'unknown'
    
    def scan_project(self, *, printer=None) -> Dict[str, Any]:
        """Main method to scan the project and return structured data"""
        tree, _ = self.generate_tree(printer=printer, depth=0)
        framework = self.detect_framework()
        
        # Get project name, fallback to current directory name if empty
        project_name = self.root_path.name
        if not project_name or project_name == '.':
            project_name = self.root_path.resolve().name
        
        return {
            "metadata": {
                "project_name": project_name,
                "framework": framework,
                "scan_date": datetime.now().isoformat(),
                "root_path": str(self.root_path.resolve())
            },
            "tree": tree
        }
