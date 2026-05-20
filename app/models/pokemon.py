from pydantic import BaseModel
from typing import Optional


class PokemonCreate(BaseModel):
    alias: str
    id: int
    family: str
    generation: str
    ReleaseDate: str


class PokemonResponse(BaseModel):
    alias: str
    id: int
    family: str
    generation: str
    ReleaseDate: str
    goShadowReleased: Optional[bool] = None
    goShadowRelease: Optional[str] = None
