import jwt, requests

from django.conf   import settings
from django.http   import JsonResponse

from users.models  import User
from .excepts       import Kakaoerror

def login_decorator(func):

    def wrapper(self, request, *args, **kwargs):
        try:
            token         = request.headers.get("Authorization", None)
            token_payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
            user          = User.objects.get(id=token_payload['user_id'])
            request.user  = user

            return func(self, request, *args, **kwargs) 

        except jwt.DecodeError:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=401)
            
    return wrapper

class KakaoAPI:
    def __init__(self,KAKAO_REST_API_KEY, KAKAO_REDIRECT_URI):
        self.kakao_rest_api_key = KAKAO_REST_API_KEY
        self.kakao_redirect_uri = KAKAO_REDIRECT_URI
        self.access_token       = None

    def get_kakao_token(self, code):
        auth_code       = code
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        data            = {
            "grant_type"      : 'authorization_code',
            "client_id"       : self.kakao_rest_api_key,
            "redirect_uri"    : self.kakao_redirect_uri,
            "code"            : auth_code
        }
        headers  = {'Content-type' : 'application/x-www-form-urlencoded;charset=utf-8'}
        response = requests.post(kakao_token_api, headers=headers, data=data, timeout=3)

        if not response.ok:
            # return JsonResponse({'message' : 'INVALID_RESPONSE'}, status=401)
            raise Kakaoerror("INVALID_RESPONSE", 401)

        self.access_token = response.json().get('access_token')
        return self.access_token
        
    def get_kakao_profile(self, access_token):
        headers = {
            "Authorization" : f'Bearer {access_token}',
            "Content-type"  : "application/x-www-form-urlencoded;charset=utf-8"
        }
        
        response = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers)
        
        if not response.ok:
            # return JsonResponse({'message' : 'INVALID_RESPONSE'}, status=401)
            raise Kakaoerror("INVALID_RESPONSE", 401)
        
        return response.json()