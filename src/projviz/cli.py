import click
import json
import time
from pathlib import Path
from .scanner import ProjectScanner
from .server import start_server

@click.group()
def main():
    """Project VizTree - Python project structure visualizer"""
    pass

@main.command()
@click.option('--path', default='.', help='Path to the project directory')
@click.option('--output', '-o', default='project_structure.json', 
              help='Output JSON file name')
@click.option('--list', 'list_paths', is_flag=True,
              help='Print all files and folders in sorted order while scanning')
@click.option('--ignore', multiple=True, help='Additional ignore patterns (can be repeated)')
def scan(path, output, list_paths, ignore):
    """Scan project structure and generate JSON output"""
    try:
        t0 = time.perf_counter()
        scanner = ProjectScanner(path)
        if ignore:
            scanner.ignore_patterns.extend(ignore)

        printer = None
        if list_paths:
            root_name = Path(path).resolve().name
            def _printer(kind, relpath, depth):
                indent = '  ' * depth
                label = relpath if relpath else root_name
                if kind == 'folder':
                    # =foldername
                    click.echo(f"{indent}={Path(label).name}")
                else:
                    # -filename.ext
                    click.echo(f"{indent}-{Path(label).name}")
            printer = _printer

        result = scanner.scan_project(printer=printer)
        t1 = time.perf_counter()
        
        with open(output, 'w') as f:
            json.dump(result, f, indent=2)
        
        click.echo(f"Project structure saved to {output}")
        click.echo(f"Detected framework: {result['metadata']['framework']}")
        click.echo(f"Project name: {result['metadata']['project_name']}")

        # Additional scan report
        def _count(node):
            folders = 0
            files = 0
            if not isinstance(node, dict):
                return folders, files
            if node.get('type') == 'folder':
                folders += 1
                for child in node.get('data', []) or []:
                    f2, f3 = _count(child)
                    folders += f2
                    files += f3
            else:
                files += 1
            return folders, files

        folders, files = _count(result.get('tree', {}))
        total_nodes = folders + files
        root_children = len((result.get('tree') or {}).get('data', []) or [])
        duration_ms = int((t1 - t0) * 1000)

        click.echo(
            f"Scan report: nodes={total_nodes} (folders={folders}, files={files}), "
            f"root_children={root_children}, duration={duration_ms}ms"
        )
    except Exception as e:
        click.echo(f"Error scanning project: {e}", err=True)
        raise click.Abort()

@main.command()
@click.option('--json-file', '-j', default='project_structure.json', 
              help='JSON file with project structure')
@click.option('--port', '-p', default=8000, help='Port to run the server on')
@click.option('--host', '-h', default='localhost', help='Host to bind the server to')
def serve(json_file, port, host):
    """Start visualization server (Bootstrap UI)"""
    if not Path(json_file).exists():
        click.echo(f"Error: JSON file {json_file} not found. Run 'scan' first.", err=True)
        raise click.Abort()
    
    click.echo(f"Starting visualization server on http://{host}:{port}")
    click.echo("Press Ctrl+C to stop the server")
    try:
        start_server(json_file, host, port)
    except KeyboardInterrupt:
        click.echo("\nServer stopped.")
    except Exception as e:
        click.echo(f"Error starting server: {e}", err=True)
        raise click.Abort()

@main.command()
@click.option('--path', default='.', help='Path to the project directory')
@click.option('--output', '-o', default='project_structure.json', 
              help='Output JSON file name')
@click.option('--port', '-p', default=8000, help='Port to run the server on')
@click.option('--host', '-h', default='localhost', help='Host to bind the server to')
def run(path, output, port, host):
    """Scan project and start server in one command"""
    # First scan the project
    scan_ctx = click.Context(scan)
    scan_ctx.invoke(scan, path=path, output=output)
    
    # Then start the server
    serve_ctx = click.Context(serve)
    serve_ctx.invoke(serve, json_file=output, port=port, host=host)

if __name__ == '__main__':
    main()
