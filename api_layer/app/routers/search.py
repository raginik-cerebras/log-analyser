from fastapi import APIRouter, Depends, Query, HTTPException
from app.deps import require_api_key
from app.services.elastic import search
from app.config import settings
import logging

# ------------------------------
# Logging setup
# ------------------------------
logger = logging.getLogger("api_layer")

router = APIRouter(prefix="/search", tags=["search"])

@router.get('/errors', summary="Search for errors using wildcard")
async def search_errors(
    pattern: str = Query(..., description='Substring or token to search (e.g., "Error", "Exception")'),
    days: int = settings.default_days,
    size: int = 100,
    api_key: str = Depends(require_api_key)
):
    """
    Search for logs containing a specific error pattern using a wildcard query.
    
    This endpoint uses a wildcard query on the `message.keyword` field, which is useful for 
    finding exact substring matches that might be part of a larger token.
    
    - **pattern**: The text pattern to search for (e.g., "NullPointer").
    - **days**: Number of days in the past to search.
    - **size**: Maximum number of results to return.
    """
    logger.info(f"API Request: GET /search/errors?pattern={pattern}&days={days}&size={size}")

    body = {
        "query": {
            "bool": {
                "must": [{"wildcard": {"message.keyword": f"*{pattern}*"}}],
                "filter": [{"range": {"@timestamp": {"gte": f"now-{days}d"}}}]
            }
        },
        # "size": size,  <-- REMOVED: Passed as kwarg to search()
        "sort": [{"@timestamp": {"order": "desc"}}]
    }

    try:
        res = search(settings.index_pattern, body, size=size)
        hits = [h["_source"] for h in res.get("hits", {}).get("hits", [])]
        total = res.get("hits", {}).get("total", {}).get("value", 0)
        
        logger.info(f"Found {total} error logs matching pattern '{pattern}'")
        return {"total": total, "results": hits}
        
    except Exception as e:
        logger.error(f"Error executing search_errors with pattern='{pattern}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error during search")


@router.get('/pattern', summary="General pattern search")
async def search_pattern(
    pattern: str = Query(..., description='Lucene query string or simple text'),
    days: int = settings.default_days,
    size: int = 100,
    api_key: str = Depends(require_api_key)
):
    """
    Perform a general search using a query string.
    
    This endpoint uses the `query_string` query, which supports Lucene syntax (e.g., "error AND fatal")
    and searches across multiple message fields (`message`, `log.message`, `event.original`).
    It is analyzer-friendly and generally faster for full-text search than wildcards.
    
    - **pattern**: The search query (e.g., "error", "failed AND critical").
    - **days**: Number of days in the past to search.
    - **size**: Maximum number of results to return.
    """
    logger.info(f"API Request: GET /search/pattern?pattern={pattern}&days={days}&size={size}")

    body = {
        "query": {
            "bool": {
                "must": [{"query_string": {"query": pattern, "fields": ["message", "log.message", "event.original"]}}],
                "filter": [{"range": {"@timestamp": {"gte": f"now-{days}d"}}}]
            }
        },
        # "size": size, <-- REMOVED: Passed as kwarg to search()
        "sort": [{"@timestamp": {"order": "desc"}}]
    }

    try:
        res = search(settings.index_pattern, body, size=size)
        hits = [h["_source"] for h in res.get("hits", {}).get("hits", [])]
        total = res.get("hits", {}).get("total", {}).get("value", 0)

        logger.info(f"Found {total} logs matching pattern '{pattern}'")
        return {"total": total, "results": hits}

    except Exception as e:
        logger.error(f"Error executing search_pattern with pattern='{pattern}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error during search")