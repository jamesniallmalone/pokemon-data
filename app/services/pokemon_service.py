import boto3

from app.config import AWS_REGION, TABLE_NAME

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

table = dynamodb.Table(TABLE_NAME)


def get_pokemon(alias: str, pokemon_id: int):

    response = table.get_item(
        Key={
            "alias": alias,
            "id": pokemon_id
        }
    )

    return response.get("Item")


def create_pokemon(item: dict):

    table.put_item(Item=item)

    return item


def update_shadow_status(
    alias: str,
    pokemon_id: int,
    release_date: str
):

    table.update_item(
        Key={
            "alias": alias,
            "id": pokemon_id
        },

        UpdateExpression="""
            SET
                goShadowReleased = :released,
                goShadowRelease = :releaseDate
        """,

        ExpressionAttributeValues={
            ":released": True,
            ":releaseDate": release_date
        }
    )

    return {
        "alias": alias,
        "id": pokemon_id,
        "goShadowReleased": True,
        "goShadowRelease": release_date
    }


def delete_pokemon(alias: str, pokemon_id: int):

    table.delete_item(
        Key={
            "alias": alias,
            "id": pokemon_id
        }
    )

    return True
