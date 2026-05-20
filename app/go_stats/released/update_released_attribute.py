import boto3
from boto3.dynamodb.conditions import Attr
from tqdm import tqdm
import time
from botocore.exceptions import ClientError
import sys

from release_list import GORELEASE_POKEMON

# ==========================================
# OPTIONAL DATE FILTER
# ==========================================

DATE_FILTER = None

if len(sys.argv) > 1:
    DATE_FILTER = sys.argv[1]

# ==========================================
# CONFIG
# ==========================================

TABLE_NAME = "pokemon-master"
AWS_REGION = "eu-west-1"

# ==========================================
# DYNAMODB SETUP
# ==========================================

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

# ==========================================
# FILTER DATASET
# ==========================================

pokemon_to_update = GORELEASE_POKEMON

if DATE_FILTER:

    pokemon_to_update = [
        p for p in GORELEASE_POKEMON
        if p["date"] > DATE_FILTER
    ]

    print(f"Filtering entries newer than {DATE_FILTER}")

print(f"{len(pokemon_to_update)} Pokémon will be updated")


# ==========================================
# UPDATE LOOP
# ==========================================
print(f"Updating {len(GORELEASE_POKEMON)} Pokémon...")

success_count = 0
failure_count = 0

for pokemon in tqdm(
    pokemon_to_update,
    desc="Updating Released Pokémon"
):

    alias = pokemon["alias"]
    pokemon_id = pokemon["id"]
    release_date = pokemon["goReleasedDate"]

    while True:

        try:

            table.update_item(
                Key={
                    "alias": alias,
                    "id": pokemon_id
                },

                UpdateExpression="""
                    SET
                        goReleased = :released,
                        goReleasedDate = :releaseDate
                """,

                ExpressionAttributeValues={
                    ":released": True,
                    ":releaseDate": release_date
                }
            )

            success_count += 1
            break

        except ClientError as e:
            failure_count += 1
            print(f"\nRetrying {alias} (#{pokemon_id})")
            print(e.response["Error"]["Message"])
            time.sleep(1)

# ==========================================
# COMPLETE
# ==========================================

print("\n===================================")
print("Update Complete")
print("===================================")
print(f"Successful Updates: {success_count}")
print(f"Failed Attempts: {failure_count}")
print("===================================")