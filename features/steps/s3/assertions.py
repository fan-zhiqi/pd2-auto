from retrying import retry

import features.steps.s3.other as s3_other


@retry(wait_fixed=5000, stop_max_attempt_number=10)
def assert_actor_can_access_buckets(context, actor, bucket_names):
    """ Assert an actor can access a bucket in AWS

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: string
    :param bucket_names: name of buckets to look for
    :type  bucket_names: str
    """

    bucket_names_from_s3 = s3_other.get_s3_bucket_names(context, actor)
    bucket_name_list = bucket_names.split(',')

    assert set(bucket_name_list) == set(bucket_names_from_s3)


@retry(wait_fixed=5000, stop_max_attempt_number=20)
def assert_total_number_of_files_in_s3_bucket(context, actor, n, bucket_name):
    """ Check there is the correct number of files in the s3 bucket

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: string
    :param n: expected number of files
    :type  n: int
    :param bucket_name: name of bucket files should be in
    :type  bucket_name: str
    """
    files = s3_other.get_files_in_s3_bucket(context, actor, bucket_name)

    assert len(files) == n, \
        f'Bucket {bucket_name} does not contain correct number of files, ' \
        f'got {len(files)} expected {n}'
