import json, boto3, uuid
from unicodedata import category

from django.http        import JsonResponse
from django.views       import View
from django.conf        import settings

from projects.models    import Organization, Project, ProjectImage, Category
from core.utils         import login_decorator

class S3ImgUploader(View):
    def post(self, request):
        s3_client = boto3.client(
            's3',
            aws_access_key_id     = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        )

        file = request.FILES.get('formData', None)

        url = 'img'+'/'+uuid.uuid1().hex
        
        s3_client.upload_fileobj(
            file, 
            "greeneeds", 
            url, 
            ExtraArgs={
                "ContentType": file.content_type
            }
        )
        return JsonResponse({"MESSAGE" : "UPLOAD_SUCCESS"}, status = 201)