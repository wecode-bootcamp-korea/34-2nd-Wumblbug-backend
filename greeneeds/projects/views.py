from datetime           import date

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Count

from projects.models    import Project


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

