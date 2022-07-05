from django.db       import models

from projects.models import Project, Organization
from users.models    import User
from core.models     import TimeStampModel

class Donation(TimeStampModel):
    project      = models.ForeignKey(Project, on_delete=models.CASCADE)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "donations"