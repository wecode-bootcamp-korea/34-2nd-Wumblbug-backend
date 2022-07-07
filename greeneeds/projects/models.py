from django.db    import models

from core.models  import TimeStampModel
import users

class Project(TimeStampModel):
    user            = models.ForeignKey('users.User', on_delete=models.CASCADE)
    category        = models.ForeignKey("Category", on_delete=models.CASCADE)
    title           = models.CharField(max_length=70)
    shortcut_title  = models.CharField(max_length=50)
    summary         = models.CharField(max_length=100)
    total_amount    = models.DecimalField(max_digits=9, decimal_places=2)
    price           = models.DecimalField(max_digits=7, decimal_places=2)
    thumbnail       = models.URLField(max_length=150)
    pk_uri          = models.CharField(max_length=50, unique=True)
    target_amount   = models.DecimalField(max_digits=9, decimal_places=2)
    start_datetime  = models.DateField()
    end_datetime    = models.DateField()
    pay_end_date    = models.DateField()
    settlement_date = models.DateField()
    introduction    = models.CharField(max_length=200)
    budget_plan     = models.CharField(max_length=200)
    organizations   = models.ManyToManyField("Organization", through="ProjectOrganization", related_name="project")

    class Meta:
        db_table = "projects"

class Category(models.Model):
    name      = models.CharField(max_length=50)
    image_url = models.URLField(max_length=150)

    class Meta:
        db_table = "categories"

class ProjectImage(models.Model):
    project   = models.ForeignKey(Project, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=150)

    class Meta:
        db_table = "project_images"

class Tag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name    = models.CharField(max_length=50)

    class Meta:
        db_table = "tags"

class Organization(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "organizations"

class ProjectOrganization(models.Model):
    project      = models.ForeignKey(Project, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        db_table = "projects_organizations"