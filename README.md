# Pokemon API

FastAPI + DynamoDB CRUD API for Pokemon metadata.

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker

```bash
docker build -t pokemon-api .
docker run -p 8000:8000 pokemon-api
```

## Swagger Docs

Open:

http://localhost:8000/docs
