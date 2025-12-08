from fastapi import APIRouter, Depends, HTTPException
from app.services.elastic import search
from app.config import settings
from app.deps import require_api_key
import logging

# ------------------------------
# Logging setup
# ------------------------------
logger = logging.getLogger("api_layer")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = True

# ------------------------------
# Router
# ------------------------------
router = APIRouter(prefix="/logs", tags=["logs"])

# ------------------------------
# Helper: Build ES query
# ------------------------------
def make_query(must_filters, days):
    """
    Constructs the Elasticsearch query body.
    """
    return {
        "sort": [{"@timestamp": {"order": "asc"}}],
        "query": {
            "bool": {
                "must": must_filters,
                "filter": [{"range": {"@timestamp": {"gte": f"now-{days}d"}}}]
            }
        }
    }

# ------------------------------
# Helper: Build message clause
# ------------------------------
def build_message_clause(pattern):
    """
    Builds the search clause for the message field.
    Uses 'match' for full-text search capabilities (case-insensitive).
    """
    return {"match": {"message": pattern}}

# ------------------------------
# Generic function to fetch logs
# ------------------------------
def fetch_logs(id_field, id_value, pattern=None, days=30, size=100):
    """
    Executes the search against Elasticsearch.
    
    Args:
        id_field: The field name to filter by (e.g., 'train_id').
        id_value: The value of the ID.
        pattern: Optional text pattern to search in the message.
        days: Number of days to look back.
        size: Max number of logs to return.
    """
    logger.info(f"Fetching logs for {id_field}={id_value}, pattern='{pattern}', days={days}, size={size}")
    
    must = [{"term": {f"{id_field}.keyword": id_value}}]

    if pattern:
        must.append(build_message_clause(pattern))

    body = make_query(must, days)
    logger.debug(f"Elasticsearch query body: {body}")

    try:
        res = search(settings.index_pattern, body, size=size)
    except Exception as e:
        logger.error(f"Error querying Elasticsearch for {id_field}={id_value}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error during log retrieval")

    hits_count = res.get('hits', {}).get('total', {}).get('value', 0)
    logger.info(f"Found {hits_count} logs for {id_field}={id_value}")
    
    return [hit["_source"] for hit in res.get("hits", {}).get("hits", [])]

# ------------------------------
# /logs/train/{train_id}
# ------------------------------
@router.get("/train/{train_id}", summary="Get logs by Train ID")
async def logs_for_train(
    train_id: str,
    pattern: str = None,
    days: int = settings.default_days,
    size: int = 100,
    api_key: str = Depends(require_api_key)
):
    """
    Retrieve logs associated with a specific Train ID.

    - **train_id**: The unique identifier for the training job.
    - **pattern**: Optional keyword or phrase to filter log messages (case-insensitive).
    - **days**: Number of days in the past to search (default: configured default).
    - **size**: Maximum number of log entries to return (default: 100).
    """
    logger.info(f"API Request: GET /logs/train/{train_id}")
    return fetch_logs("train_id", train_id, pattern, days, size)

# ------------------------------
# /logs/test/{test_id}
# ------------------------------
@router.get("/test/{test_id}", summary="Get logs by Test ID")
async def logs_for_test(
    test_id: str,
    pattern: str = None,
    days: int = settings.default_days,
    size: int = 100,
    api_key: str = Depends(require_api_key)
):
    """
    Retrieve logs associated with a specific Test ID.

    - **test_id**: The unique identifier for the test job.
    - **pattern**: Optional keyword or phrase to filter log messages.
    - **days**: Number of days in the past to search.
    - **size**: Maximum number of log entries to return.
    """
    logger.info(f"API Request: GET /logs/test/{test_id}")
    return fetch_logs("test_id", test_id, pattern, days, size)

# ------------------------------
# /logs/file/{file_name}
# ------------------------------
@router.get("/file/{file_name}", summary="Get logs by File Name")
async def logs_for_file(
    file_name: str,
    pattern: str = None,
    days: int = settings.default_days,
    size: int = 100,
    api_key: str = Depends(require_api_key)
):
    """
    Retrieve logs associated with a specific file name.

    - **file_name**: The name of the file to filter logs by.
    - **pattern**: Optional keyword or phrase to filter log messages.
    - **days**: Number of days in the past to search.
    - **size**: Maximum number of log entries to return.
    """
    logger.info(f"API Request: GET /logs/file/{file_name}")
    return fetch_logs("file_name", file_name, pattern, days, size)
