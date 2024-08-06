import logging
import traceback

import boto3
from botocore.exceptions import NoCredentialsError

from src.config import settings

logger = logging.getLogger("app")


class S3CloudStorageHandler:
    def __init__(self, config):
        # Set your MinIO credentials and endpoint
        self.minio_access_key = config.S3_ACCESS_KEY
        self.minio_secret_key = config.S3_SECRET_ACCESS_KEY
        self.minio_endpoint = "https://hb.vkcs.cloud"  # 'http://minio-server:9000'
        self.source_bucket_name = "test-bucket-1"
        self.destination_bucket_name = "test-bucket-2"
        self.region_name = "ru-msk"
        self.service_name = "s3"

    # Create an S3 client
    def get_s3_client(self):
        try:
            s3 = boto3.client(
                "s3",
                endpoint_url=self.minio_endpoint,
                aws_access_key_id=self.minio_access_key,
                aws_secret_access_key=self.minio_secret_key,
            )
            return s3
        except NoCredentialsError:
            logger.error("Credentials not available")
        except Exception as e:
            logger.error(f"Exception occurred while creating S3 client: {e}")
            traceback.print_exc()

    # Create a bucket if not exists
    def create_minio_bucket(self, bucket_name):
        # Create a bucket in MinIO
        try:
            s3 = self.get_s3_client()

            # Check if the bucket already exists
            response = s3.list_buckets()
            existing_buckets = [
                bucket["Name"] for bucket in response.get("Buckets", [])
            ]

            if bucket_name in existing_buckets:
                logger.info(f"Bucket {bucket_name} already exists")
            else:
                s3.create_bucket(Bucket=bucket_name)
                logger.info(f"Bucket {bucket_name} created successfully")
        except NoCredentialsError:
            logger.error("Credentials not available")

    # Check if an object exists in a bucket
    def check_object_exists(self, source_bucket_name, object_name):
        # Check if an object exists in MinIO
        try:
            s3 = self.get_s3_client()
            s3.head_object(Bucket=source_bucket_name, Key=object_name)
            logger.info(f"Object {object_name} exists in {source_bucket_name}")
        except NoCredentialsError:
            logger.error("Credentials not available")
        except s3.exceptions.NoSuchKey:
            logger.info(f"Object {object_name} does not exist in {source_bucket_name}")

    # Check if an object from one bucket to another
    def copy_object(
        self,
        source_bucket_name,
        source_object_name,
        destination_bucket_name,
        destination_object_name,
    ):
        # Copy an object in MinIO
        try:
            # Ensure the destination bucket exists
            self.create_minio_bucket(destination_bucket_name)

            s3 = self.get_s3_client()
            s3.copy_object(
                Bucket=destination_bucket_name,
                CopySource={"Bucket": source_bucket_name, "Key": source_object_name},
                Key=destination_object_name,
            )
            logger.info(
                f"Object {source_bucket_name}/{source_object_name} copied to {destination_bucket_name}/{destination_object_name}"
            )
        except NoCredentialsError:
            logger.error("Credentials not available")

    # Delete an object from bucket
    def delete_object(self, bucket_name, object_name):
        # Delete an object from MinIO bucket
        try:
            s3 = self.get_s3_client()
            s3.delete_object(Bucket=bucket_name, Key=object_name)
            logger.info(f"Object {object_name} deleted from {bucket_name}")
        except NoCredentialsError:
            logger.error("Credentials not available")

    # Upload data from local to S3 bucket
    def upload_to_s3(self, file_path, bucket_name, object_name):
        # Upload a file to MinIO
        try:
            s3 = self.get_s3_client()
            # Create bucket if not exists
            self.create_minio_bucket(bucket_name)
            # Upload the file to s3 bucket
            s3.upload_file(file_path, bucket_name, object_name)
            logger.info(f"File uploaded successfully to {bucket_name}/{object_name}")
        except FileNotFoundError:
            logger.error("The file was not found")
        except NoCredentialsError:
            logger.error("Credentials not available")

    # Download data from S3 bucket to local
    def download_from_s3(self, source_bucket_name, object_name, local_file_path):
        # Download a file from MinIO
        try:
            s3 = self.get_s3_client()
            s3.download_file(source_bucket_name, object_name, local_file_path)
            logger.info(f"File downloaded successfully to local [{local_file_path}]")
        except NoCredentialsError:
            logger.error("Credentials not available")


s3_cloud_storage_handler = S3CloudStorageHandler(settings)
