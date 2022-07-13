import json
from core.excepts import Kakaoerror
from datetime import date

import jwt
from django.views    import View
from django.http     import JsonResponse
from django.conf     import settings

from core.utils   import KakaoAPI, login_decorator
from users.models import User
from core.utils      import KakaoAPI
from core.utils      import login_decorator
from users.models    import User, Like
from projects.models import Project

class KakaoSigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            code = data['code']

            kakao_api = KakaoAPI(settings.KAKAO_REST_API_KEY, settings.KAKAO_REDIRECT_URI)

            kakao_token   = kakao_api.get_kakao_token(code)
            kakao_profile = kakao_api.get_kakao_profile(kakao_token)

            user, is_created = User.objects.get_or_create(
                kakao_id = kakao_profile['id'],
                defaults = {
                    'email'    : kakao_profile['kakao_account']['email'],
                    'nickname' : kakao_profile['properties']['nickname']
                }
            )

            status_code = 201 if is_created else 200

            access_token = jwt.encode({'user_id': user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            return JsonResponse({'token': access_token}, status=status_code)
                
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)
        except Kakaoerror as e:
            return JsonResponse({'MESSAGE' : e.message}, status = e.status)

class UserView(View):
    @login_decorator
    def get(self, request):
        user = request.user

        result = {
            'user_id'  : user.id,
            'nickname' : user.nickname,
            'email'    : user.email
        }
        return JsonResponse({'result': result}, status=200)
class LikeView(View):  
    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = request.user
            project_id = data['project_id']
            project    = Project.objects.get(id=project_id)

            if Like.objects.filter(user=user, project=project).exists():
                Like.objects.filter(user=user, project=project).delete()
                like_count = Like.objects.filter(project=project).count()
                return JsonResponse({'message': 'SUCCESS', 'like_count':like_count}, status=200)

            Like.objects.create(
                project = project,
                user    = user
            )
            like_count = Like.objects.filter(project=project).count()

            return JsonResponse({'message': 'SUCCESS', 'like_count': like_count}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except Project.DoesNotExist:
            return JsonResponse({"message" : "PROJECT_DOES_NOT_EXIST"}, status=400)

    @login_decorator
    def get(self, request):
        user          = request.user
        like_projects = Like.objects.filter(user=user)
        today         = date.today()

        like_projects = [
            {
                "user_id"       : user.id,
                "project_id"    : like_project.project.id,
                "thumbnail"     : like_project.project.thumbnail,
                "category"      : like_project.project.category.name,
                "title"         : like_project.project.title,
                "summary"       : like_project.project.summary,
                "total_amount"  : int(like_project.project.total_amount),
                "remain_days"   : (like_project.project.end_datetime - today).days
            } for like_project in like_projects
        ]

        return JsonResponse({'result' : like_projects}, status=200)
