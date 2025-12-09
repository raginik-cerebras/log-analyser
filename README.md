# Log Archival & Analysis API

A high-performance FastAPI service designed to query, filter, and analyze archived logs stored in Elasticsearch. This tool enables engineers to quickly triage failures by searching across training jobs, tests, and log files.

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

#### Option 1: Local Development
1. **Install Dependencies**:  
   Run the following command to install the required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
2. **Start Server**:
   Run the following command to start the server
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
#### Option 2: Docker
   Run the following command to build docker
   ```bash
   docker-compose up --build
   ```

## 🔑 Authentication

All endpoints require an API key. Pass the API key in the request header as follows:  
- **Header**: `x-api-key`  
- **Value**: The value defined in your `.env` file.

## 📝 Example Usage

### 1. Log Retrieval
##  Get logs for a specific Train ID:
   ```bash
    curl -X 'GET' \
    'http://localhost:8000/logs/train/696924ce11e4710857cf5a058e?pattern=Error&days=30&size=50' \
    -H 'accept: application/json' \
    -H 'x-api-key: default_api_key'
   ```
##  Get logs for a specific Test ID:
   ```bash
    curl -X 'GET' \
    'http://localhost:8000/logs/test/test_12345?pattern=Failed&days=7' \
    -H 'accept: application/json' \
    -H 'x-api-key: default_api_key'
   ```
##  Get logs for a specific File Name:
   ```bash
    curl -X 'GET' \
    'http://localhost:8000/logs/file/syslog.log?pattern=Critical&days=1' \
    -H 'accept: application/json' \
    -H 'x-api-key: default_api_key' 
   ```

### 2. Search
## General Pattern Search (Lucene Syntax): Supports complex queries like error AND "connection timeout".
   ```bash 
   curl -X 'GET' \
  'http://localhost:8000/search/pattern?pattern=error%20AND%20timeout&days=7' \
  -H 'accept: application/json' \
  -H 'x-api-key: default_api_key'
   ```
## Search for errors (Wildcard): Useful for finding substrings like *NullPointer*.
   ```bash
      curl -X 'GET' \
   'http://localhost:8000/search/errors?pattern=NullPointer&days=7' \
   -H 'accept: application/json' \
   -H 'x-api-key: default_api_key'
   ```

### 3. Statistics
## Find files containing a pattern:
   ```bash
      curl -X 'GET' \
   'http://localhost:8000/stats/files?pattern=IOError&days=30' \
   -H 'accept: application/json' \
   -H 'x-api-key: default_api_key'
  ```

## Find training jobs containing a pattern:
   ```bash
      curl -X 'GET' \
   'http://localhost:8000/stats/trains?pattern=CUDA_ERROR&days=30' \
   -H 'accept: application/json' \
   -H 'x-api-key: default_api_key'
   ```
## Get error frequency timeline:
   ```bash
      curl -X 'GET' \
   'http://localhost:8000/stats/errors/timeline?pattern=Error&days=90' \
   -H 'accept: application/json' \
   -H 'x-api-key: default_api_key'
  ```
