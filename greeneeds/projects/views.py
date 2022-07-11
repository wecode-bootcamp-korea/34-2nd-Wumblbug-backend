from datetime import date

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Count

from projects.models import Project


class ProjectDetailView(View):
     def get(self, request, project_id):
          try:
               project = Project.objects.annotate(like_count=Count('like__id')).get(id=project_id)             
               
               images = [{
                 "id"  : image.id,
                 "url" : image.image_url
               } for image in project.projectimage_set.all()]

               organizations = [{
                    "id"  : org.id,
                    "name": org.name
               } for org in project.organizations.all()]
             
               results = {
                    'id'             : int(project.id),
                    'thumbmail'      : project.thumbnail,
                    'category'       : project.category.name,
                    'title'          : project.title,
                    'like_count'     : project.like_count,
                    'target_amount'  : int(project.target_amount), 
                    'price'          : int(project.price),
                    'start_datetime' : project.start_datetime,
                    'end_datetime'   : project.end_datetime,
                    'pay_end_date'   : project.pay_end_date,
                    'settlement_date': project.settlement_date,
                    'introduction'   : project.introduction,
                    'budget_plan'    : project.budget_plan,
                    'total_amount'   : int(project.total_amount),
                    'organizations'  : organizations,
                    'images'         : images,
                    'remain_days'    : (project.end_datetime - date.today()).days
               }

               return JsonResponse({'results' : results}, status = 200)
          except Project.DoesNotExist:
               return JsonResponse({'message' : 'PROJECT_DOES_NOT_EXIST'}, status = 400)