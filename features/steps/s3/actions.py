from features.steps.context_management import get_actor_client, \
    add_to_scenario_data
from features.steps.utils import list_local_dir, path_to_local_file
from features.tuples import S3Bucket, S3File


def create_s3_bucket(context, actor, bucket_name):
    """

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: string
    :param bucket_name: name of bucket to create
    :type  bucket_name: str
    """
    client = get_actor_client(context, actor)
    bucket = client.create_bucket(bucket_name)

    s3_bucket = S3Bucket(
        alias=bucket_name,
        bucket=bucket
    )
    client.wait_for_bucket_exists(bucket_name)

    add_to_scenario_data(context, what=s3_bucket, where='buckets')


def upload_file_to_s3(context, actor, file, bucket_name, desired_file_path):
    """

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: str
    :param file: name of file in /files to upload to s3
    :type  file: str
    :param bucket_name: name of bucket to upload file to
    :type  bucket_name: str
    :param desired_file_path: desired file path in s3
    :type  desired_file_path: str
    """
    client = get_actor_client(context, actor)

    client.upload_file(
        bucket_name=bucket_name,
        file=file,
        desired_file_path=desired_file_path
    )

    file_in_s3 = S3File(
        alias=desired_file_path,
        bucket_name=bucket_name,
        owner=actor
    )

    add_to_scenario_data(context, where='files', what=file_in_s3)


def upload_directory_to_s3_with_contents(
        context, actor, directory_name, bucket_name):
    """ Upload all the contents of a directory to s3 and keep the relative
    paths

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: string
    :param directory_name: name of directory in /files to upload to s3
    :type  directory_name: str
    :param bucket_name: name of bucket to upload files to
    :type  bucket_name: str
    :return:
    """
    directory_contents = list_local_dir(directory_name)

    for f in directory_contents:
        relative_path = path_to_local_file(f'{directory_name}/{f}')
        upload_file_to_s3(
            context,
            actor,
            file=relative_path,
            bucket_name=bucket_name,
            desired_file_path=f
        )
