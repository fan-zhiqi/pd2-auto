from retrying import retry

from features.steps.context_management import delete_from_scenario_data
from features.steps.context_management import get_actor_client


@retry(wait_fixed=5000, stop_max_attempt_number=10)
def delete_created_buckets(context):
    """ Delete buckets from s3 instance created as part of the tests

    :param context: behave Context
    :type  context: behave.runner.Context
    """

    if not context.scenario_data.buckets:
        return

    created_buckets = context.scenario_data.buckets[:]

    for bucket in created_buckets:

        # Sometimes the deleting files fails in minio, stopping you from being
        # able to delete a bucket, this retry loop ensures success
        s3_bucket = bucket.bucket
        s3_bucket.objects.all().delete()

        if list(s3_bucket.objects.all()):
            raise RuntimeError('Failed to delete objects from s3 instance')

        res = bucket.bucket.delete()

        assert res['ResponseMetadata']['HTTPStatusCode'] == 204, \
            'Unable to delete created bucket'
        delete_from_scenario_data(context, what=bucket, where='buckets')


@retry(wait_fixed=2000, stop_max_attempt_number=10)
def delete_uploaded_files(context):
    """ Delete uploaded files from s3 instance created as part of the tests

    :param context: behave Context
    :type  context: behave.runner.Context
    """

    if not context.scenario_data.files:
        return

    uploaded_files = context.scenario_data.files[:]

    for file_ in uploaded_files:
        client = get_actor_client(context, file_.owner)
        client.delete_file(file_.bucket_name, file_.alias)
        delete_from_scenario_data(context, what=file_, where='files')


@retry(wait_fixed=2000, stop_max_attempt_number=10)
def logout(context):
    """ Logout as current User

    :param context: behave Context
    :type  context: behave.runner.Context
    """

    if not context.scenario_data.tokens:
        return

    logout_users = context.scenario_data.tokens[:]

    for logout_ in logout_users:
        client = get_actor_client(context, logout_.actor)
        client.v1.logout()
        delete_from_scenario_data(context, what=logout_, where='tokens')
