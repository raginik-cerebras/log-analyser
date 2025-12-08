# api_layer


FastAPI-based triage API for ELK logs.


## Run with Docker


1. Copy .env.example to .env and set API_KEY
2. Build image: docker build -t api_layer:latest .
3. Run (on same docker network as Elasticsearch):
docker run -d --name api_layer --env-file .env --network <your-network> -p 8000:8000 api_layer:latest


