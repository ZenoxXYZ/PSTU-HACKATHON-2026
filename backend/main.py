from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.errors import AppError
from backend.routes import auth, users

app = FastAPI(title="Money Movement Application")

app.include_router(auth.router)
app.include_router(users.router)


@app.exception_handler(AppError)
def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )


@app.get("/", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/health", tags=["health"])
def api_health() -> dict[str, str]:
    return {"status": "ok"}
