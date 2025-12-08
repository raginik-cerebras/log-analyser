from elasticsearch import Elasticsearch
from app.config import settings
import logging

# ------------------------------
# Logging setup
# ------------------------------
logger = logging.getLogger("api_layer")

es = Elasticsearch(settings.elasticsearch_url)

# helper wrapper functions

def search(index_pattern, body, size=10000):
    """
    Executes a standard search query against Elasticsearch.

    Args:
        index_pattern (str): The index or pattern to search (e.g., "logs-*").
        body (dict): The Elasticsearch query DSL body.
        size (int): The maximum number of documents to return. Defaults to 10000.

    Returns:
        dict: The raw Elasticsearch response.
    """
    logger.debug(f"Executing search on index='{index_pattern}' with size={size}. Body: {body}")
    try:
        response = es.search(index=index_pattern, body=body, size=size)
        hits = response.get('hits', {}).get('total', {}).get('value', 0)
        logger.debug(f"Search successful. Found {hits} hits.")
        return response
    except Exception as e:
        logger.error(f"Elasticsearch search failed: {e}")
        raise


def agg_search(index_pattern, body):
    """
    Executes an aggregation search query against Elasticsearch.
    
    This function forces size=0 to only return aggregation results, not documents.

    Args:
        index_pattern (str): The index or pattern to search.
        body (dict): The Elasticsearch query DSL body containing aggregations.

    Returns:
        dict: The raw Elasticsearch response.
    """
    logger.debug(f"Executing aggregation on index='{index_pattern}'. Body: {body}")
    try:
        response = es.search(index=index_pattern, body=body, size=0)
        logger.debug("Aggregation search successful.")
        return response
    except Exception as e:
        logger.error(f"Elasticsearch aggregation failed: {e}")
        raise