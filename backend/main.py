from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.errors import AppError
from backend.routes import auth, transfers, users

app = FastAPI(title="Money Movement Application")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transfers.router)


@app.exception_handler(AppError)
def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.get("/", response_class=HTMLResponse, tags=["ui"])
def serve_dashboard() -> HTMLResponse:
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Money Movement Application</h1><p>Dashboard not yet built.</p>")


@app.get("/api/health", tags=["health"])
def api_health() -> dict[str, str]:
    return {"status": "ok"}
