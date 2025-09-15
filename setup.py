#!/usr/bin/env python3
"""
Setup script for Project VizTree
This is a fallback setup script for environments that don't support pyproject.toml
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from pyproject.toml
requirements = [
    "click >= 8.0.0",
    "fastapi >= 0.68.0",
    "uvicorn >= 0.15.0",
    "jinja2 >= 3.0.0"
]

setup(
    name="projviz",
    version="0.1.0",
    author="Nayeem Islam",
    author_email="islam.nayeem@outlook.com",
    description="Python project structure visualizer with a clean Bootstrap UI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NoManNayeem/Manchitra_SDK",
    project_urls={
        "Homepage": "https://github.com/NoManNayeem/Manchitra_SDK",
        "Repository": "https://github.com/NoManNayeem/Manchitra_SDK",
        "Issues": "https://github.com/NoManNayeem/Manchitra_SDK/issues",
        "Author": "https://www.linkedin.com/in/islamnayeem",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "projviz=projviz.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "projviz": ["templates/*.html"],
    },
)
