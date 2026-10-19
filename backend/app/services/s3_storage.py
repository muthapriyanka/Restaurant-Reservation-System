import os
from functools import lru_cache
from typing import BinaryIO

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class StorageConfigurationError(RuntimeError):
    pass


class StorageOperationError(RuntimeError):
    pass


def get_bucket_name() -> str:
    bucket = os.getenv("S3_BUCKET")
    if not bucket:
        raise StorageConfigurationError("S3_BUCKET is not configured")
    return bucket


@lru_cache
def get_s3_client():
    return boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-2"))


def upload_file(file_object: BinaryIO, object_key: str, content_type: str) -> None:
    try:
        get_s3_client().upload_fileobj(
            file_object,
            get_bucket_name(),
            object_key,
            ExtraArgs={"ContentType": content_type},
        )
    except (BotoCoreError, ClientError) as exc:
        raise StorageOperationError("Unable to upload image") from exc


def get_object(object_key: str):
    try:
        return get_s3_client().get_object(Bucket=get_bucket_name(), Key=object_key)
    except (BotoCoreError, ClientError) as exc:
        if isinstance(exc, ClientError) and exc.response.get("Error", {}).get("Code") in {
            "NoSuchKey",
            "404",
        }:
            raise FileNotFoundError(object_key) from exc
        raise StorageOperationError("Unable to read image") from exc


def delete_object(object_key: str) -> None:
    try:
        get_s3_client().delete_object(Bucket=get_bucket_name(), Key=object_key)
    except (BotoCoreError, ClientError) as exc:
        raise StorageOperationError("Unable to delete image") from exc
