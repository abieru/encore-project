from django.db import models

# Create your models here.


class IFCFilejson(models.Model):

    uploadedIfcFileUUID = models.SlugField()
    projectUUID  =models.SlugField()
    description = models.TextField(verbose_name='Description')
    name = models.CharField(max_length=200, verbose_name='file name')
    userU = models.CharField(max_length=200, verbose_name='user who uploaded')
    IFCjson =models.JSONField(verbose_name="ifc json file")
    dateAndTime = models.CharField(max_length=500, default=None)

