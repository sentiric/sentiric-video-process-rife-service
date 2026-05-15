import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging_utils import setup_logging
from app.core.engine import rife_engine
from app.grpc_server import serve_grpc

setup_logging("video-process-rife-service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    rife_engine.initialize()
    task = asyncio.create_task(serve_grpc())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)
@app.get("/healthz")
def health(): return {"status": "ok", "service": "video-process-rife-service"}