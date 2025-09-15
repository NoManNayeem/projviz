from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import json
from pathlib import Path
import uvicorn
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

def start_server(json_file: str, host: str = 'localhost', port: int = 8000):
    """Start the FastAPI server with Bootstrap-based interface"""
    app = FastAPI(title="Project VizTree")
    logger = logging.getLogger("projviz.server")
    logger.info("Initializing server: json_file=%s host=%s port=%s", json_file, host, port)
    
    # Set up templates
    templates_path = Path(__file__).parent / "templates"
    templates = Jinja2Templates(directory=templates_path)
    
    # Load project data
    with open(json_file, 'r') as f:
        project_data = json.load(f)
    try:
        meta = project_data.get("metadata", {})
        logger.info("Loaded project metadata: name=%s framework=%s", meta.get("project_name"), meta.get("framework"))
    except Exception as e:
        logger.warning("Unable to read project metadata: %s", e)

    # Resolve project root directory (for file content API)
    root_dir = None
    try:
        meta_root = project_data.get("metadata", {}).get("root_path")
        if meta_root:
            root_dir = Path(meta_root).resolve()
        else:
            root_dir = Path(json_file).resolve().parent
        logger.info("Project root directory set to %s", root_dir)
    except Exception:
        root_dir = Path(json_file).resolve().parent
    
    # Serve static files (optional assets)
    static_path = templates_path / "static"
    if static_path.exists():
        logger.info("Mounting static assets from %s", static_path)
        app.mount("/static", StaticFiles(directory=static_path), name="static")
    else:
        logger.info("No static assets directory found at %s (using CDN)", static_path)
    
    @app.get("/", response_class=HTMLResponse)
    async def read_root(request: Request):
        logger.info("GET / -> render tree.html")
        return templates.TemplateResponse("tree.html", {
            "request": request,
            "project_name": project_data["metadata"]["project_name"],
            "framework": project_data["metadata"]["framework"]
        })
    
    @app.get("/api/tree")
    async def get_tree():
        logger.info("GET /api/tree")
        try:
            payload = project_data["tree"]
            # Lightweight visibility into the shape/size of data
            if isinstance(payload, list):
                logger.info("/api/tree -> list with %d root items", len(payload))
            elif isinstance(payload, dict):
                logger.info("/api/tree -> dict with keys: %s", list(payload.keys())[:10])
            else:
                logger.info("/api/tree -> type=%s", type(payload).__name__)
            return JSONResponse(payload)
        except KeyError as e:
            logger.exception("KeyError serving /api/tree: %s", e)
            return JSONResponse({"error": f"missing key: {e}"}, status_code=500)
        except Exception as e:
            logger.exception("Unexpected error serving /api/tree: %s", e)
            return JSONResponse({"error": str(e)}, status_code=500)
    
    @app.get("/diagram")
    async def get_diagram(request: Request):
        logger.info("GET /diagram -> render diagram.html")
        return templates.TemplateResponse("diagram.html", {
            "request": request,
            "project_name": project_data["metadata"]["project_name"]
        })

    @app.get("/uml")
    async def get_uml(request: Request):
        logger.info("GET /uml -> render uml.html")
        return templates.TemplateResponse("uml.html", {
            "request": request,
            "project_name": project_data["metadata"]["project_name"]
        })
    
    @app.get("/api/metadata")
    async def get_metadata():
        logger.info("GET /api/metadata")
        try:
            return JSONResponse(project_data["metadata"])
        except Exception as e:
            logger.exception("Error serving /api/metadata: %s", e)
            return JSONResponse({"error": str(e)}, status_code=500)

    @app.get("/api/file")
    async def get_file(path: str):
        """Return text content of a file within the project root.
        Limits response size to prevent huge payloads.
        """
        logger.info("GET /api/file path=%s", path)
        if not path:
            raise HTTPException(status_code=400, detail="Missing path parameter")
        # Normalize and security check
        target = (root_dir / path).resolve()
        try:
            target.relative_to(root_dir)
        except ValueError:
            raise HTTPException(status_code=403, detail="Path outside project root")
        if not target.exists() or not target.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        # Read with size limit
        try:
            max_bytes = 512 * 1024  # 512KB
            data = target.read_bytes()
            truncated = len(data) > max_bytes
            if truncated:
                data = data[:max_bytes]
            try:
                text = data.decode('utf-8')
                encoding = 'utf-8'
            except UnicodeDecodeError:
                # Fallback to latin-1 to at least display something
                text = data.decode('latin-1', errors='replace')
                encoding = 'latin-1'
            return JSONResponse({
                "path": path,
                "encoding": encoding,
                "truncated": truncated,
                "size": target.stat().st_size,
                "content": text
            })
        except Exception as e:
            logger.exception("Error reading file %s: %s", target, e)
            raise HTTPException(status_code=500, detail=str(e))
    
    logger.info("Starting uvicorn at http://%s:%s", host, port)
    uvicorn.run(app, host=host, port=port, log_level="info")
