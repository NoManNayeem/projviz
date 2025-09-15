#!/usr/bin/env python3
"""
Example usage of Project VizTree
"""

import json
from pathlib import Path
from src.projviz.scanner import ProjectScanner
from src.projviz.framework_detection import FrameworkDetector

def main():
    """Demonstrate Project VizTree functionality"""
    
    # Example 1: Basic project scanning
    print("=== Project VizTree Example ===\n")
    
    # Scan current directory
    current_dir = Path.cwd()
    print(f"Scanning project: {current_dir.name}")
    
    scanner = ProjectScanner(str(current_dir))
    result = scanner.scan_project()
    
    print(f"Project Name: {result['metadata']['project_name']}")
    print(f"Detected Framework: {result['metadata']['framework']}")
    print(f"Scan Date: {result['metadata']['scan_date']}")
    
    # Example 2: Framework detection details
    print("\n=== Framework Detection Details ===")
    detector = FrameworkDetector(current_dir)
    framework = detector.detect_framework()
    framework_info = detector.get_framework_info(framework)
    
    print(f"Framework: {framework_info['name']}")
    print(f"Description: {framework_info['description']}")
    print(f"Website: {framework_info['website']}")
    
    # Example 3: Save project structure to JSON
    output_file = "example_project_structure.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\nProject structure saved to: {output_file}")
    
    # Example 4: Display tree structure (simplified)
    print("\n=== Project Tree Structure ===")
    def print_tree(node, indent=0):
        prefix = "  " * indent
        icon = "📁" if node['type'] == 'folder' else "📄"
        print(f"{prefix}{icon} {node['value']}")
        
        if node['type'] == 'folder' and 'data' in node:
            for child in node['data'][:5]:  # Show first 5 items
                print_tree(child, indent + 1)
            if len(node['data']) > 5:
                print(f"{prefix}  ... and {len(node['data']) - 5} more items")
    
    print_tree(result['tree'])
    
    print(f"\nTo start the web server, run:")
    print(f"projviz serve --json-file {output_file} --port 8000")
    print(f"Then open http://localhost:8000 in your browser")

if __name__ == "__main__":
    main()
