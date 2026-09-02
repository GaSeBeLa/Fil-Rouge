# creer_buckets.py
import os
import boto3
from botocore.exceptions import ClientError
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / "docker" / ".env")
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",   # à retirer le jour où on passe sur du vrai AWS S3
    aws_access_key_id=os.environ["MINIO_ROOT_USER"],
    aws_secret_access_key=os.environ["MINIO_ROOT_PASSWORD"],
)

for name in ["bronze", "silver", "gold"]:
    try:
        s3.create_bucket(Bucket=name)
        print(f"✅ Bucket créé : {name}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            print(f"ℹ️  Bucket déjà existant : {name}")
        else:
            raise

print([b["Name"] for b in s3.list_buckets()["Buckets"]])