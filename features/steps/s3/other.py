from features.steps.context_management import get_actor_client


def get_s3_buckets(context, actor):
    """ Get buckets from s3 instance

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: string
    :return: list of buckets available to user in s3 instance
    :rtype: list
    """
    s3 = get_actor_client(context, actor)
    return s3.list_buckets()


def get_s3_bucket_names(context, actor):
    """ Get names of buckets in s3 instance

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: string
    :return: list of buckets available to user in s3 instance
    :rtype: list
    """
    return [bucket.name for bucket in get_s3_buckets(context, actor)]


def get_files_in_s3_bucket(context, actor, bucket_name):
    """ Get files present in s3 bucket

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: string
    :param bucket_name: Name of bucket to get files from
    :type  bucket_name: str
    :return: list of files as dicts
    :rtype: list
    """
    s3 = get_actor_client(context, actor)
    return s3.list_files(bucket_name)
