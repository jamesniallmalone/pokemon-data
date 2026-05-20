import json
import time
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from tqdm import tqdm

# ============================================
# CONFIG
# ============================================

TABLE_NAME = "pokemon-master"
AWS_REGION = "eu-north-1"
INPUT_DIR = "regionDex"

# DynamoDB batch_write_item limit
BATCH_SIZE = 25

# ============================================
# DYNAMODB SETUP
# ============================================

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

# ============================================
# LOAD ALL JSON FILES
# ============================================

json_files = sorted("pokemon*.json")

if not json_files:
    raise Exception(f"No JSON files found in: {INPUT_DIR}")

print(f"Found {len(json_files)} JSON files")

# ============================================
# PROCESS FILES
# ============================================

total_written = 0
total_failed = 0

for json_file in json_files:

    print(f"\nProcessing {json_file.name}")

    with open(json_file, "r", encoding="utf-8") as f:
        pokemon_data = json.load(f)

    print(f"Loaded {len(pokemon_data)} Pokémon")

    # ============================================
    # CHUNK INTO DYNAMODB BATCHES
    # ============================================

    batches = [
        pokemon_data[i:i + BATCH_SIZE]
        for i in range(0, len(pokemon_data), BATCH_SIZE)
    ]

    # ============================================
    # UPLOAD BATCHES
    # ============================================

    with tqdm(total=len(pokemon_data), desc=json_file.name) as progress_bar:

        for batch in batches:

            request_items = [
                {
                    "PutRequest": {
                        "Item": item
                    }
                }
                for item in batch
            ]

            success = False

            while not success:
                try:

                    response = table.meta.client.batch_write_item(
                        RequestItems={
                            TABLE_NAME: request_items
                        }
                    )

                    unprocessed = response.get("UnprocessedItems", {})

                    # Retry unprocessed items automatically
                    while unprocessed and unprocessed.get(TABLE_NAME):

                        print(
                            f"Retrying {len(unprocessed[TABLE_NAME])} unprocessed items..."
                        )

                        time.sleep(1)

                        response = table.meta.client.batch_write_item(
                            RequestItems=unprocessed
                        )

                        unprocessed = response.get("UnprocessedItems", {})

                    success = True

                    total_written += len(batch)
                    progress_bar.update(len(batch))

                except ClientError as e:

                    total_failed += len(batch)

                    print("\nBatch failed")
                    print(e.response["Error"]["Message"])

                    # Retry after brief delay
                    time.sleep(2)

# ============================================
# SUMMARY
# ============================================

print("\n============================================")
print("IMPORT COMPLETE")
print("============================================")

print(f"Files processed : {len(json_files)}")
print(f"Pokémon written : {total_written}")
print(f"Pokémon failed  : {total_failed}")