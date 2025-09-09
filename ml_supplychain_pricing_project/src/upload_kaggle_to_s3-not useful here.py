# src/upload_kaggle_to_s3.py

import os
import subprocess
import boto3
import shutil
import zipfile

# -----------------------------
# 1️⃣ AWS CONFIGURATION
# -----------------------------
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
bucket_name = "ml-supplychain-project"  # change to your bucket

s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# -----------------------------
# 2️⃣ KAGGLE CONFIGURATION
# -----------------------------
kernel_identifier = "divyeshardeshana/supply-chain-shipment-price-data-analysis"
temp_folder = "temp_kaggle"
os.makedirs(temp_folder, exist_ok=True)

# -----------------------------
# 3️⃣ DOWNLOAD KAGGLE KERNEL OUTPUT
# -----------------------------
print(f"Downloading Kaggle kernel output to {temp_folder} ...")
result = subprocess.run([
    "kaggle", "kernels", "output", kernel_identifier,
    "-p", temp_folder
], capture_output=True, text=True)

if result.returncode != 0:
    print("Error downloading from Kaggle:")
    print(result.stderr)
    exit(1)
else:
    print(result.stdout)

# -----------------------------
# 4️⃣ UNZIP ANY ZIP FILES IF PRESENT
# -----------------------------
def unzip_if_needed(file_path, extract_to):
    if zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Unzipped {file_path}")
        os.remove(file_path)

for f in os.listdir(temp_folder):
    file_path = os.path.join(temp_folder, f)
    unzip_if_needed(file_path, temp_folder)

# -----------------------------
# 5️⃣ CHECK FILES BEFORE UPLOAD
# -----------------------------
files_to_upload = [f for f in os.listdir(temp_folder) if os.path.isfile(os.path.join(temp_folder, f))]
if not files_to_upload:
    print("No files found to upload. Exiting.")
    exit(1)

print("Files to upload:")
for f in files_to_upload:
    print(f)

# -----------------------------
# 6️⃣ UPLOAD FILES TO S3
# -----------------------------
for f in files_to_upload:
    local_path = os.path.join(temp_folder, f)
    s3_key = f"raw/{f}"  # path inside S3 bucket
    try:
        s3.upload_file(local_path, bucket_name, s3_key)
        print(f"Uploaded {f} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading {f}: {e}")

# -----------------------------
# 7️⃣ CLEAN UP TEMPORARY FILES
# -----------------------------
shutil.rmtree(temp_folder)
print(f"Temporary folder {temp_folder} deleted.")
print("All files uploaded to S3 successfully!")
