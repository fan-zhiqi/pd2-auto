from collections import namedtuple

ScenarioData = namedtuple(
    'ScenarioData', (
        'actors '
        'buckets '
        'files '
        'tokens '
        'aliases'
    )
)

Actor = namedtuple(
    'Actor', (
        'alias '
        'client '
        'type'
    )
)

NetworkData = namedtuple(
    'NetworkData', (
        'minio '
        'api '
        'rabbit '
        'rabbit_api'
    )
)

S3Bucket = namedtuple(
    'Bucket', (
        'alias '
        'bucket'
    )
)

S3File = namedtuple(
    'File', (
        'alias '
        'bucket_name '
        'owner'
    )
)

Token = namedtuple(
    'Token', (
        'alias '
        'actor '
        'email '
        'token'
    )
)

SiteAlias = namedtuple(
    'SiteAlias', (
        'alias '
        'actor '
        'name '
        'id'
    )
)
