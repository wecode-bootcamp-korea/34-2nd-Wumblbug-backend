import json, jwt, requests

from django.views     import View
from django.http      import JsonResponse
from django.conf      import settings

from core.utils       import KakaoLoginAPI
from users.models     import User

class KakaoSigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            code = data['code']
            kakao_api = KakaoLoginAPI()

            kakao_api.get_kakao_token(code)
            kakao_profile = kakao_api.get_kakao_profile()

            user, is_created = User.objects.get_or_create(
                kakao_id = kakao_profile['id'],
                defaults = {
                    'email'    : kakao_profile['kakao_account']['email'],
                    'nickname' : kakao_profile['properties']['nickname']
                }
            )

            access_token = jwt.encode({'user_id': user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            return JsonResponse({'token': access_token}, status=201)
                
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)