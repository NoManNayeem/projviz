"""
Project VizTree - Python project structure visualizer
"""

__version__ = "0.1.0"
__author__ = "Project VizTree Team"

from .scanner import ProjectScanner
from .cli import main

__all__ = ["ProjectScanner", "main"]
