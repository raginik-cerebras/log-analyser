from fastapi import FastAPI
from app.routers import search, stats, logs
from app.config import settings
import logging

# ------------------------------
# Logging setup
# ------------------------------
# Configure basic logging for the application
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("api_layer.main")

app = FastAPI(
    title='Triage API', 
    description="API for querying and analyzing archived logs from Elasticsearch.",
    version='1.0'
)


app.include_router(search.router)
app.include_router(stats.router)
app.include_router(logs.router)


@app.on_event("startup")
async def startup_event():
    """
    Log application startup and configuration.
    """
    logger.info("Starting up Triage API...")
    logger.info(f"Connected to Elasticsearch at {settings.elasticsearch_url}")


@app.get('/', summary="Root endpoint")
async def root():
    """
    Root endpoint to verify service reachability.
    """
    logger.debug("Root endpoint called")
    return {"status": "ok", "service": "triage-api"}

@app.get("/health", summary="Health check")
async def health():
    """
    Health check endpoint for monitoring tools (e.g., Docker, Kubernetes).
    """
    return {"status": "ok"}