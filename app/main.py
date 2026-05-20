from fastapi import FastAPI
from app.routes import pokemon

app = FastAPI(
    title="Pokemon API",
    version="1.0.0"
)

app.include_router(
    pokemon.router,
    prefix="/pokemon",
    tags=["Pokemon"]
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
