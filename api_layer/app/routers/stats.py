from fastapi import APIRouter, Depends, Query, HTTPException
from app.deps import require_api_key
from app.services.elastic import agg_search
from app.config import settings
import logging

# ------------------------------
# Logging setup
# ------------------------------
logger = logging.getLogger("api_layer")
# Ensure handlers are set up if not already configured globally
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = True

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get('/files', summary="Get files containing pattern")
async def files_with_pattern(
    pattern: str = Query(..., description="Pattern to search for (wildcard)"),
    days: int = settings.default_days,
    size: int = 100,
    api_key: str = Depends(require_api_key)
):
    """
    Identify files that contain a specific log pattern.
    
    - **pattern**: The text pattern to search for (wildcard search on message).
    - **days**: Number of days in the past to search.
    - **size**: Maximum number of file names to return.
    """
    logger.info(f"API Request: GET /stats/files?pattern={pattern}&days={days}&size={size}")

    body = {
        "size": 0,
        "query": {
            "bool": {
                "must": [{"wildcard": {"message.keyword": f"*{pattern}*"}}],
                "filter": [{"range": {"@timestamp": {"gte": f"now-{days}d"}}}]
            }
        },
        "aggs": {"files": {"terms": {"field": "file_name.keyword", "size": size}}}
    }

    try:
        res = agg_search(settings.index_pattern, body)
        buckets = res.get('aggregations', {}).get('files', {}).get('buckets', [])
        logger.info(f"Found {len(buckets)} files matching pattern '{pattern}'")
        return {"files": buckets}
    except Exception as e:
        logger.error(f"Error in files_with_pattern: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get('/trains', summary="Get trains containing pattern")
async def trains_with_pattern(
    pattern: str = Query(..., description="Pattern to search for (wildcard)"),
    days: int = settings.default_days,
    size: int = 1000,
    api_key: str = Depends(require_api_key)
):
    """
    Identify training jobs (train_id) that contain a specific log pattern.
    
    - **pattern**: The text pattern to search for.
    - **days**: Number of days in the past to search.
    - **size**: Maximum number of train IDs to return.
    """
    logger.info(f"API Request: GET /stats/trains?pattern={pattern}&days={days}&size={size}")

    body = {
        "size": 0,
        "query": {
            "bool": {
                "must": [{"wildcard": {"message.keyword": f"*{pattern}*"}}],
                "filter": [{"range": {"@timestamp": {"gte": f"now-{days}d"}}}]
            }
        },
        "aggs": {"trains": {"terms": {"field": "train_id.keyword", "size": size}}}
    }

    try:
        res = agg_search(settings.index_pattern, body)
        buckets = res.get('aggregations', {}).get('trains', {}).get('buckets', [])
        logger.info(f"Found {len(buckets)} trains matching pattern '{pattern}'")
        return {"trains": buckets}
    except Exception as e:
        logger.error(f"Error in trains_with_pattern: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get('/tests', summary="Get tests containing pattern")
async def tests_with_pattern(
    pattern: str = Query(..., description="Pattern to search for (wildcard)"),
    days: int = settings.default_days,
    size: int = 500,
    api_key: str = Depends(require_api_key)
):
    """
    Identify test jobs (test_id) that contain a specific log pattern.
    
    - **pattern**: The text pattern to search for.
    - **days**: Number of days in the past to search.
    - **size**: Maximum number of test IDs to return.
    """
    logger.info(f"API Request: GET /stats/tests?pattern={pattern}&days={days}&size={size}")

    body = {
        "size": 0,
        "query": {
            "bool": {
                "must": [{"wildcard": {"message.keyword": f"*{pattern}*"}}],
                "filter": [{"range": {"@timestamp": {"gte": f"now-{days}d"}}}]
            }
        },
        "aggs": {"tests": {"terms": {"field": "test_id.keyword", "size": size}}}
    }

    try:
        res = agg_search(settings.index_pattern, body)
        buckets = res.get('aggregations', {}).get('tests', {}).get('buckets', [])
        logger.info(f"Found {len(buckets)} tests matching pattern '{pattern}'")
        return {"tests": buckets}
    except Exception as e:
        logger.error(f"Error in tests_with_pattern: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get('/errors/timeline', summary="Get error frequency over time")
async def errors_timeline(
    pattern: str = Query(..., description="Pattern to search for (wildcard)"),
    days: int = 30,
    api_key: str = Depends(require_api_key)
):
    """
    Get a histogram of how often a pattern appears over time.
    
    - **pattern**: The text pattern to search for.
    - **days**: Number of days in the past to search.
    """
    logger.info(f"API Request: GET /stats/errors/timeline?pattern={pattern}&days={days}")

    body = {
        "size": 0,
        "query": {
            "bool": {
                "must": [{"wildcard": {"message.keyword": f"*{pattern}*"}}],
                "filter": [{"range": {"@timestamp": {"gte": f"now-{days}d"}}}]
            }
        },
        "aggs": {"errors_over_time": {"date_histogram": {"field": "@timestamp", "calendar_interval": "day"}}}
    }

    try:
        res = agg_search(settings.index_pattern, body)
        aggs = res.get('aggregations', {})
        logger.info(f"Retrieved timeline stats for pattern '{pattern}'")
        return aggs
    except Exception as e:
        logger.error(f"Error in errors_timeline: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")