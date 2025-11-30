import boto3

# AWS credentials (use your own keys)
aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
region_name = 'us-east-1'  # adjust if needed

# S3 setup
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

bucket_name = 'your-bucket-name'
file_path = '../data/your_dataset.csv'  # relative path from src/
s3_key = 'raw/your_dataset.csv'         # path in S3 bucket

# Upload file
try:
    s3.upload_file(file_path, bucket_name, s3_key)
    print(f"File {file_path} uploaded to s3://{bucket_name}/{s3_key}")
except Exception as e:
    print(f"Error uploading file: {e}")
