import boto3
from botocore.client import Config as BotoConfig
from botocore.exceptions import ClientError

ALLOWED_IMAGE_TYPES = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}

class Storage:
    def __init__(self):
        self._s3 = None
        self._bucket = None

    def init_storage(self, app):
        app.extensions["storage"] = self
        if not app.config.get("S3_ENDPOINT"):
            app.logger.warning("S3_ENDPOINT is not set: picture storage is disabled")
            return

        self._bucket = app.config["S3_BUCKET"]
        self._s3 = boto3.client(
            "s3",
            endpoint_url=app.config["S3_ENDPOINT"],
            aws_access_key_id=app.config["S3_ACCESS_KEY"],
            aws_secret_access_key=app.config["S3_SECRET_KEY"],
            region_name="us-east-1",
            config=BotoConfig(s3={"addressing_style": "path"}),
        )

    def check_bucket(self):
        try:
            self._s3.head_bucket(Bucket=self._bucket)
        except ClientError:
            try:
                self._s3.create_bucket(Bucket=self._bucket)
            except ClientError as e:
                if e.response["Error"]["Code"] not in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
                    raise


    def is_enabled(self) -> bool:
        return self._s3 is not None


    def upload(self, data, key, content_type):
        self._s3.put_object(Bucket=self._bucket, Key=key, Body=data, ContentType=content_type)


    def download(self, key):
        obj = self._s3.get_object(Bucket=self._bucket, Key=key)
        return obj["Body"].read(), obj.get("ContentType", "application/octet-stream")

 