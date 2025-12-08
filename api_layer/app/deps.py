from fastapi import Header, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from app.config import settings
import logging

# ------------------------------
# Logging setup
# ------------------------------
logger = logging.getLogger("api_layer.deps")

# Define the API Key header scheme for OpenAPI documentation
api_key_header = APIKeyHeader(name='x-api-key', auto_error=False)


async def require_api_key(api_key: str = Security(api_key_header)):
    """
    Dependency to validate the API key provided in the 'x-api-key' header.
    
    This function checks if the header is present and matches the configured secret.
    
    Raises:
        HTTPException(401): If the API key is missing or invalid.
    """
    if not api_key:
        logger.warning("Authentication failed: Missing 'x-api-key' header")
        raise HTTPException(status_code=401, detail="Missing API Key")
        
    if api_key != settings.api_key:
        logger.warning("Authentication failed: Invalid API Key provided")
        raise HTTPException(status_code=401, detail="Invalid API Key")
        
    return api_key