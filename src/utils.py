import asyncio
import logging
import os
import shutil
from uuid import uuid4

from src.config import settings, upload_dir_path
from src.models import FileMetadataORM
from src.repository import FileRepository
from src.s3_storage import s3_cloud_storage_handler

logger = logging.getLogger("app")


def get_file_uid():
    return str(uuid4())


def get_file_extension(filename):
    return os.path.splitext(filename)[1]


def get_file_path_with_extension(file_uid, file_extension):
    return os.path.join(upload_dir_path, file_uid) + file_extension


def get_file_name(file_uid, file_extension):
    return file_uid + file_extension


def write_file(file_bytes, file_path):
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file_bytes, buffer)


async def save_file_metadata_to_db(file, file_uid, file_extension, file_path):
    file_metadata = FileMetadataORM(
        uid=file_uid,
        original_name=file.filename,
        size=os.path.getsize(file_path),
        content_type=file.content_type,
        extension=file_extension,
    )

    await FileRepository.save_single_item_to_db(file_metadata)
    return file_metadata


async def upload_file_to_cloud(file_path: str, file_name: str):
    if settings.S3_STORAGE_ACTIVE:
        s3_cloud_storage_handler.create_minio_bucket(
            s3_cloud_storage_handler.source_bucket_name
        )
        s3_cloud_storage_handler.upload_to_s3(
            file_path, s3_cloud_storage_handler.source_bucket_name, file_name
        )
    else:
        # Имитация отправки файла в облако
        await asyncio.sleep(1)
        logger.info(f"File {file_name} uploaded to cloud storage.")
