import boto3
from lib.sussyconfig import get_config

config = get_config()

MINIO_CONF = config.S3_CONFIG

BUCKET_NAME = config.S3_BUCKET_NAME

s3_client = boto3.client('s3', **MINIO_CONF)

def get_public_url(object_name):
    endpoint = MINIO_CONF['endpoint_url'].rstrip('/')
    object_name = object_name.replace(" ", "%20")
    return f"{endpoint}/{BUCKET_NAME}/{object_name}"

def list_images(prefix='', return_names=False):
    paginator = s3_client.get_paginator('list_objects_v2')
    
    page_iterator = paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix)

    file_list = []

    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                file_key = obj['Key']
                if file_key.endswith('/'):
                    continue
                if return_names:
                    file_list.append(file_key.split('/')[-1])
                    continue
                url = get_public_url(file_key)
                file_list.append(url)
    
    return file_list