from django.db import models

from .validators import validate_file_extension

class IFCFilejson(models.Model):
    """
    Model to convert ifc to json from encore
    """

    uploadedIfcFileUUID = models.SlugField()
    projectUUID  =models.SlugField()
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    name = models.CharField(max_length=200, verbose_name='file name')
    userU = models.CharField(max_length=200, verbose_name='user who uploaded')
    IFCjson =models.JSONField(verbose_name="ifc json file")
    dateAndTime = models.CharField(max_length=500, default=None, blank=True, null=True)



class IfcConvertModel(models.Model):

    """
        Model for send ifc file  with a post requests
    """
    projectUUID = models.SlugField()
    uploadedIfcFileUUID = models.SlugField()
    name = models.CharField(max_length=200, verbose_name='file name')
    userU = models.CharField(max_length=200, verbose_name='user who uploaded')
    IFCFile =  models.FileField(upload_to='files/IFCFile_model', validators=[validate_file_extension])

class IfcResultModel(models.Model):
    """
        Model results of ifc file to json data
    """
    IfcFileID = models.OneToOneField(IfcConvertModel,on_delete=models.CASCADE, primary_key=True)
    IFCjsonResult = models.JSONField(verbose_name="json files")