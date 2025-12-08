from pydantic import BaseSettings, Field
import logging

# ------------------------------
# Logging setup
# ------------------------------
logger = logging.getLogger("api_layer.config")

class Settings(BaseSettings):
    """
    Application configuration settings.
    
    These settings are loaded from environment variables or a .env file.
    """
    api_key: str = Field(..., description="Secret API key for authentication (header: x-api-key)")
    elasticsearch_url: str = Field("http://elasticsearch:9200", description="URL of the Elasticsearch instance")
    index_pattern: str = Field("cs1_logs-*", description="Elasticsearch index pattern to query")
    default_days: int = Field(7, description="Default number of days to search back if not specified")

    class Config:
        env_file = ".env"

# Instantiate settings
try:
    settings = Settings()
    # Log non-sensitive configuration on startup to verify environment
    logger.info(f"Config loaded: ES_URL={settings.elasticsearch_url}, Index={settings.index_pattern}, DefaultDays={settings.default_days}")
except Exception as e:
    # If config fails (e.g. missing api_key), log critical error
    logger.critical(f"Failed to load application configuration: {e}")
    raise