import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")
TABLE_NAME = os.getenv("TABLE_NAME", "Pokemon")
