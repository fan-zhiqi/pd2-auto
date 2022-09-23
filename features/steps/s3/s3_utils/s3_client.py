import boto3
from botocore.client import Config as BotoConfig


class S3Client:

    def __init__(self, url, access_key, secret_key, **kwargs):
        self.url = url,
        self.access_key = access_key,
        self.secret_key = secret_key,
        self.config = kwargs

        self._session = boto3.session.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            **kwargs
        )

        self._resource = self._session.resource(
            's3',
            endpoint_url=url,
            config=BotoConfig(signature_version='s3v4'),
            use_ssl=False,
            **kwargs
        )

        self._client = self._session.client(
            's3',
            endpoint_url=url,
            config=BotoConfig(signature_version='s3v4'),
            use_ssl=False,
            **kwargs
        )

    def create_bucket(self, bucket_name: str):
        """ Create a bucket in the s3 instance

        :param bucket_name: Name of bucket to create
        :return: created s3 bucket
        :rtype: s3.Bucket
        """
        return self._resource.create_bucket(
            ACL='public-read-write',
            Bucket=bucket_name
        )

    def list_buckets(self) -> list:
        """ List the buckets in an AWS instance

        :return: list of buckets
        """
        return [bucket for bucket in self._resource.buckets.all()]

    def delete_all_buckets(self):
        """ Delete all buckets """
        for bucket in self.list_buckets():
            bucket.delete()

    def upload_file(self, bucket_name: str, file: str, desired_file_path: str):
        """ Upload a file to a bucket

        :param bucket_name: name of bucket
        :param file: path to a file
        :param desired_file_path: desired file path in the bucket
        """
        self._resource.Bucket(
            bucket_name
        ).upload_file(
            file,
            desired_file_path
        )

    def download_file(self, bucket_name: str, file: str, save_path: str):
        """ Upload a file to a bucket

        :param bucket_name: name of bucket
        :param file: path to a file in bucket
        :param save_path: desired path to save the file at
        """
        self._resource.Bucket(
            bucket_name
        ).download_file(
            file,
            save_path
        )

    def list_files(self, bucket: str) -> list:
        """ List all files in a s3 bucket

        :param bucket: Name of bucket to get files from
        :return: list of files from s3 bucket
        """
        return [
            f for f in self._client.list_objects_v2(Bucket=bucket)['Contents']]

    def delete_file(self, bucket: str, filename: str) -> None:
        """ Delete a file from s3 bucket

        :param bucket: name of bucket to delete from
        :param filename: name of file to delete
        """
        self._resource.Object(bucket, filename).delete()

    def wait_for_bucket_exists(
        self,
        bucket: str,
        delay: int=5,
        max_attempts: int=10
    ) -> None:
        """ Waits for a bucket to exist, throws an exception if does not
        exist before end of polling attempts.

        :param bucket: name of bucket to wait for
        :param delay: delay between bucket polls in seconds (default: 5)
        :param max_attempts: max number of polls for bucket (default: 10)
        """
        bucket_waiter = self._client.get_waiter('bucket_exists')

        bucket_waiter.config.delay = delay
        bucket_waiter.config.max_attempts = max_attempts

        bucket_waiter.wait(Bucket=bucket)
