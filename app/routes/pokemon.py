from fastapi import APIRouter, HTTPException

from app.models.pokemon import (
    PokemonCreate
)

from app.services.pokemon_service import (
    get_pokemon,
    create_pokemon,
    update_shadow_status,
    delete_pokemon
)

router = APIRouter()


@router.get("/{alias}/{pokemon_id}")
def fetch_pokemon(
    alias: str,
    pokemon_id: int
):

    pokemon = get_pokemon(
        alias,
        pokemon_id
    )

    if not pokemon:
        raise HTTPException(
            status_code=404,
            detail="Pokemon not found"
        )

    return pokemon


@router.post("/")
def add_pokemon(
    pokemon: PokemonCreate
):

    created = create_pokemon(
        pokemon.model_dump()
    )

    return {
        "status": "created",
        "pokemon": created
    }


@router.patch("/{alias}/{pokemon_id}/shadow")
def set_shadow_status(
    alias: str,
    pokemon_id: int,
    release_date: str
):

    updated = update_shadow_status(
        alias,
        pokemon_id,
        release_date
    )

    return {
        "status": "updated",
        "pokemon": updated
    }


@router.delete("/{alias}/{pokemon_id}")
def remove_pokemon(
    alias: str,
    pokemon_id: int
):

    delete_pokemon(
        alias,
        pokemon_id
    )

    return {
        "status": "deleted"
    }
