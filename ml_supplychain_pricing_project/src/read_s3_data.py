import os
import boto3
import pandas as pd
from io import StringIO

# AWS S3 CONFIGURATION
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
bucket_name = "ml-supplychain-project"  # change to your bucket
s3_key = "raw/train.csv"  # change to your file path in S3

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Download file from S3 and read into pandas DataFrame
try:
    print(f"Reading {s3_key} from s3://{bucket_name} ...")
    obj = s3.get_object(Bucket=bucket_name, Key=s3_key)
    df = pd.read_csv(obj['Body'])
    print("Data read successfully!")
    print(df.head())
except Exception as e:
    print(f"Error reading file from S3: {e}")
