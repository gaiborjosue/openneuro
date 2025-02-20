"""Environment based configuration."""

import os


# Configuration specific to the datalad-service
DATALAD_WORKERS = int(os.getenv('DATALAD_WORKERS', 1))
DATALAD_GITHUB_ORG = os.getenv('DATALAD_GITHUB_ORG')
DATALAD_GITHUB_LOGIN = os.getenv('DATALAD_GITHUB_LOGIN')
DATALAD_GITHUB_PASS = os.getenv('DATALAD_GITHUB_PASS')
DATALAD_GITHUB_TOKEN = os.getenv('DATALAD_GITHUB_TOKEN')
DATALAD_GITHUB_EXPORTS_ENABLED = os.getenv('DATALAD_GITHUB_EXPORTS_ENABLED')
DATALAD_S3_PUBLIC_ON_EXPORT = os.getenv('DATALAD_S3_PUBLIC_ON_EXPORT')

# Configuration shared with OpenNeuro or AWS CLI
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_ACCOUNT_ID = os.getenv('AWS_ACCOUNT_ID')
AWS_S3_PRIVATE_BUCKET = os.getenv('AWS_S3_PRIVATE_BUCKET')
AWS_S3_PUBLIC_BUCKET = os.getenv('AWS_S3_PUBLIC_BUCKET')
JWT_SECRET = os.getenv('JWT_SECRET')

# Sentry monitoring
SENTRY_DSN = os.getenv('SENTRY_DSN')

# GraphQL URL - override if not docker-compose
GRAPHQL_ENDPOINT = os.getenv('GRAPHQL_ENDPOINT', 'http://server:8111/crn/graphql')

# Redis Host
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')

# The path to connect to Elastic APM server
ELASTIC_APM_SERVER_URL = os.getenv('ELASTIC_APM_SERVER_URL')

# Elasticsearch URL
ELASTICSEARCH_CONNECTION = os.getenv('ELASTICSEARCH_CONNECTION')

# Site URL
CRN_SERVER_URL = os.getenv('CRN_SERVER_URL')
