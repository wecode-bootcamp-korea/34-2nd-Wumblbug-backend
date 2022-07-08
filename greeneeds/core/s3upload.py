import boto3
import uuid

from django.conf import settings

class MyS3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        boto3_s3 = boto3.client(
            's3',
            aws_access_key_id     = access_key,
            aws_secret_access_key = secret_key
        )
        self.s3_client   = boto3_s3
        self.bucket_name = bucket_name

    def upload(self, file):
        try: 
            url = 'img'+'/'+uuid.uuid4().hex
            extra_args = { 'ContentType' : file.content_type }
            
            self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,
                    url,
                    ExtraArgs = extra_args
                )
            return f'https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{url}'
        except:
            return None

    def delete(self, file_name):
        return self.s3_client.delete_object(bucket=self.bucket_name, Key=f'{file_name}')

s3_client = MyS3Client(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_S3_BUCKET_NAME)

class FileUpload:
    def __init__(self, client):
        self.client = client
    
    def upload(self, file):
        return self.client.upload(file)