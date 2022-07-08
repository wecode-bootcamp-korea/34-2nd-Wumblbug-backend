from datetime import date

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Count

from projects.models import Organization, Project, ProjectImage, Category
from core.utils      import login_decorator
from core.s3upload   import FileUpload, s3_client

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
          
class ProjectListView(View):
     def get(self, request):
          try:
               order_keyword = request.GET.get('order', None)
               order_prefixes = {
                    'likes' :'-like_count', 
                    'recent':'-end_datetime', 
                    'random':'?'
               }
               order = order_prefixes.get(order_keyword, 'id')
               projects = Project.objects.annotate(like_count=Count('like__id'))\
                    .order_by(order)
               
               now= date.today()
               results = [{
                    'id'            : project.id,
                    'thumbnail'     : project.thumbnail,
                    'category'      : project.category.name,              
                    'title'         : project.title,
                    'summary'       : project.summary, 
                    'target_amount' : int(project.target_amount),
                    'remain_days'   : (project.end_datetime - now).days,
                    'date'          : project.end_datetime,
                    'total_amount'  : int(project.total_amount),
                    'like_count'    : project.like_count
                    } for project in projects ]

               return JsonResponse({'results' : results}, status = 200)
          except KeyError:
               return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
          except Project.DoesNotExist:
               return JsonResponse({'message' : 'PROJECT_DOES_NOT_EXIST'}, status = 400)

     @login_decorator
     def post(self, request):
          try: 
               file           = request.FILES.get('formData', None)
               s3__client     = FileUpload(s3_client)
               upload_img_url = s3__client.upload(file)
               user           = request.user
               organizations  = Organization.objects.all()

               project = Project.objects.create(
                    user            = user,
                    category        = Category.objects.get(id=request.POST.get('category', None)),
                    title           = request.POST.get('title', None),
                    summary         = request.POST.get('summary', None),
                    target_amount   = request.POST.get('target_amount', None),
                    start_datetime  = request.POST.get('start_datetime', None),
                    end_datetime    = request.POST.get('end_datetime', None)
               )
               
               for organization in organizations:
                    project.organizations.add(organization)

               ProjectImage.objects.create(
                    image_url = upload_img_url,
                    project   = project
               )

               return JsonResponse({'message' : 'PROJECT_CREATED'}, status = 201)
          except KeyError:
               return JsonResponse({'message' : 'KEY_ERROR'}, status = 403)
