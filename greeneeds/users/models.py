from django.db       import models

from core.models     import TimeStampModel
from projects.models import Project

class User(models.Model):
    kakao_id     = models.BigIntegerField()
    email        = models.CharField(max_length=100)
    name         = models.CharField(max_length=50, null=True)
    nickname     = models.CharField(max_length=50, null=True)
    point        = models.PositiveIntegerField(default=100000)
    carbon_point = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "users"

class Like(TimeStampModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "likes"
