import requests

from django.views     import View
from django.http      import JsonResponse

from core.utils       import login_decorator

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