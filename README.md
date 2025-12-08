# Log Archival & Analysis API

A high-performance FastAPI service designed to query, filter, and analyze archived logs stored in Elasticsearch. This tool helps engineers quickly triage failures by searching across training jobs, tests, and log files.

## 🚀 Features

- **Log Retrieval**: Fetch logs by `train_id`, `test_id`, or `file_name`.
- **Full-Text Search**: Powerful search capabilities using Elasticsearch (wildcards, boolean logic).
- **Pattern Analysis**: Identify which files or tests contain specific error patterns.
- **Timeline Stats**: Visualize error frequency over time.
- **Secure**: API Key authentication via `x-api-key` header.
- **Swagger UI**: Interactive API documentation.

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Database**: Elasticsearch
- **Containerization**: Docker

## ⚙️ Configuration

Create a `.env` file in the root directory to configure the application:

```ini
# .env
API_KEY=your_secret_api_key_here
ELASTICSEARCH_URL=http://localhost:9200
INDEX_PATTERN=cs1_logs-*
DEFAULT_DAYS=7