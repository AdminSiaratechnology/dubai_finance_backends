import os
from uuid import uuid4
from decouple import config
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from fastapi import UploadFile, HTTPException

# ==============================
# ENV CONFIG
# ==============================

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_REGION_NAME = config("AWS_S3_REGION_NAME")

# ==============================
# S3 CLIENT (AWS S3)
# ==============================

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME,
)

# ==============================
# TRANSFER CONFIG
# ==============================

TRANSFER_CONFIG = TransferConfig(
    multipart_threshold=5 * 1024 * 1024,
    multipart_chunksize=5 * 1024 * 1024,
    max_concurrency=4,
    use_threads=True,
)

# ==============================
# FILE UPLOAD FUNCTION
# ==============================

async def save_upload_file(upload_file: UploadFile | None, sub_dir: str) -> str | None:
    try:
        # ✅ If file not provided
        if upload_file is None:
            return None

        allowed_types = [
            "image/jpeg",
            "image/jpg",
            "image/png",
            "application/pdf",
        ]

        if upload_file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type")

        # ✅ Extension validation
        allowed_ext = [".jpg", ".jpeg", ".png", ".pdf"]
        ext = os.path.splitext(upload_file.filename)[-1].lower()

        if ext not in allowed_ext:
            raise HTTPException(status_code=400, detail="Invalid file extension")

        # ✅ Size validation
        contents = await upload_file.read()
        file_size = len(contents)

        if file_size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large (Max 10MB)")

        await upload_file.seek(0)

        # ✅ Unique filename
        filename = f"{uuid4().hex}{ext}"
        file_path = f"{sub_dir}/{filename}"

        s3_client.upload_fileobj(
            Fileobj=upload_file.file,
            Bucket=AWS_STORAGE_BUCKET_NAME,
            Key=file_path,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": upload_file.content_type,
            },
            Config=TRANSFER_CONFIG,
        )

        file_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com/{file_path}"

        return file_url

    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"S3 Upload Failed: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")