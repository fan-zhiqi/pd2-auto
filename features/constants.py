MYSQL_DB = 'mysql'
POSTGRESQL_DB = 'postgresql'
S3_CONFIG = {
    'region_name': 'us-east-1'
}

SERVICE_HOSTS = {
    'minio': 'minio',
    'api': 'frontend_nginx',
    'rabbit': 'rabbit'
}

SERVICE_PORTS = {
    'minio': '9000',
    'api': '8888',
    'rabbit': '15672'
}

#
# # ----------------------test---------------------------------#
# # 目前用于切换组织
# organization_uuid = 'f0fb56aa-c826-4a93-a065-ea9133d4b7aa'
# # 目前用于查询show
# complex_uuids = ["4e4e8c67-21ee-47f9-881f-9c3dd10a995d"]
# PRODUCER2_URI = 'http://k8s-test-1.aamcn.com.cn:'
# PRODUCER2_CPL_URL = 'http://k8s-test-1.aamcn.com.cn:32105/cpl-service'
# PRODUCER2_PORTS = {
#     'producer2': '32101',
#     'playlist': '32110',
#     'pv-sv': '32117',
#     'content': '32158',
#     'task-sv': '32139',
#     "report-sv": '32146',
#     "complex-sv": '32102',
#     "pos-sv": '32104',
#     "agent-sv": '32103',
#     'title': '32107',
#     'site': '32102',
#     'user': '32101'
# }

# ----------------------staing---------------------------------#
# 目前用于切换组织
organization_uuid = 'e91a3e5b-fb40-4f2b-b26a-e6f6c47c6c72'
# 目前用于查询show
complex_uuids = ["f4e4a547-483a-418b-b7d6-f6d10538d5f0"]
PRODUCER2_CPL_URL = 'http://k8s-test-1.aamcn.com.cn:32105/cpl-service'
PRODUCER2_URI = 'https://'
PRODUCER2_PORTS = {
    'producer2': 'user.staging.aamts.io',
    'playlist': 'playlist-svc.staging.aamts.io',
    'pv-sv': 'producer-view.staging.aamts.io',
    'content': 'content.staging.aamts.io',
    'task-sv': 'task-service.staging.aamts.io',
    "report-sv": 'report.staging.aamts.io',
    "complex-sv": 'complex-service.staging.aamts.io',
    "pos-sv": 'pos.staging.aamts.io',
    "agent-sv": 'agent.staging.aamts.io',
    'title': 'title-service-4j.staging.aamts.io',
    'site': 'pos.staging.aamts.io',
    'user': 'user.staging.aamts.io'
}


PRODUCER2 = {
    "username": "asta.fan@artsalliancemedia.com",
    "password": "Asta123."
}

KAFAKA_HOST = "172.22.1.133"
KAFAKA_PORT = "9092"
