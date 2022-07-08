import json
from datetime         import date

from django.views     import View
from django.http      import JsonResponse

from core.utils       import login_decorator
from users.models     import Like
from projects.models  import Project

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
                return JsonResponse({'MESSAGE': 'SUCCESS', 'LIKE_COUNT':like_count}, status=201)

            Like.objects.create(
                project = project,
                user    = user
            )
            like_count = Like.objects.filter(project=project).count()

            return JsonResponse({'MESSAGE': 'SUCCESS', 'LIKE_COUNT': like_count}, status=201)
            
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=400)

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

        return JsonResponse({'RESULT' : like_projects}, status=200)
