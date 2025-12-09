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
```

## 🏃‍♂️ Running the Application
Option 1: Local Development
Install Dependencies: `pip install -r requirements.txt`

Start the Server: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

Access Documentation: Open http://localhost:8000/docs to see the interactive Swagger UI.

Option 2: Docker `docker-compose up --build`

🔑 Authentication
All endpoints require an API key. Pass it in the header:
Header: x-api-key
Value: (The value defined in your .env file)
📡 API Endpoints
1. Log Retrieval
Fetch raw logs for specific entities.

GET /logs/train/{train_id}
GET /logs/test/{test_id}
GET /logs/file/{file_name}
Parameters:

pattern (optional): Filter logs by text (e.g., "Error").
days (optional): Lookback period in days (default: 7).
size (optional): Max logs to return.

2. Search
Perform broad searches across the index.

GET /search/errors: Find logs matching a wildcard pattern (e.g., *NullPointer*).
GET /search/pattern: Full-text search using Lucene syntax (e.g., error AND "connection failed").

3. Statistics
Aggregation endpoints for high-level analysis.

GET /stats/files: Which files contain a specific pattern?
GET /stats/trains: Which training jobs contain a specific pattern?
GET /stats/errors/timeline: Histogram of errors over time.

📝 Example Usage
1. Log retrieval
Get logs for a specific Train ID:
`curl -X 'GET' \
  'http://localhost:8000/logs/train/696924ce11e4710857cf5a058e?pattern=Error&days=30&size=50' \
  -H 'accept: application/json' \
  -H 'x-api-key: default_api_key'`

Get logs for a specific Test ID:
`curl -X 'GET' \
  'http://localhost:8000/logs/test/test_12345?pattern=Failed&days=7' \
  -H 'accept: application/json' \
  -H 'x-api-key: default_api_key'`

Get logs for a specific File Name:
`curl -X 'GET' \
  'http://localhost:8000/logs/file/syslog.log?pattern=Critical&days=1' \
  -H 'accept: application/json' \
  -H 'x-api-key: default_api_key'`

2. Search
Search for errors (Wildcard): Useful for finding substrings like *NullPointer*.
`curl -X 'GET' \
  'http://localhost:8000/search/errors?pattern=NullPointer&days=7' \
  -H 'accept: application/json' \
  -H 'x-api-key: default_api_key'`

General Pattern Search (Lucene Syntax): Supports complex queries like error AND "connection timeout".

`curl -X 'GET' \
  'http://localhost:8000/search/pattern?pattern=error%20AND%20timeout&days=7' \
  -H 'accept: application/json' \
  -H 'x-api-key: default_api_key'`

3. Statistics
Find files containing a pattern:
`curl -X 'GET' \
  'http://localhost:8000/stats/files?pattern=IOError&days=30' \
  -H 'accept: application/json' \
  -H 'x-api-key: default_api_key'`

Find tests containing a pattern:
`curl -X 'GET' \
  'http://localhost:8000/stats/tests?pattern=AssertionError&days=30' \
  -H 'accept: application/json' \
  -H 'x-api-key: default_api_key'`

Get error frequency timeline:
`curl -X 'GET' \
  'http://localhost:8000/stats/errors/timeline?pattern=Error&days=90' \
  -H 'accept: application/json' \
  -H 'x-api-key: default_api_key'`
