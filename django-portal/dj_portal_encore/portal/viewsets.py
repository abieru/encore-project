from rest_framework import viewsets
from rest_framework.serializers import Serializer
import django_filters.rest_framework
from .models import IFCFilejson, IfcConvertModel, IfcResultModel
from .serializer import PortalSerializer, IfcConvertModelSerializer, IfcResultSerializer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import mimetypes
from pathlib import Path
from rest_framework.response import Response
from .PIN_DESA_PRO_PPAL_ADM_v010 import runscript1
mimetypes.add_type("text/css", ".css", True)
import json
BASE_DIR2 = Path(__file__).resolve().parent.parent
from django.shortcuts import get_object_or_404

#@method_decorator(login_required, name="dispatch")
class PortalViewSet(viewsets.ModelViewSet):
    queryset =  IFCFilejson.objects.all()
    serializer_class = PortalSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['projectUUID']
    #permission_classes = (IsAuthenticated,)
    #authentication_class = (TokenAuthentication,)



class IfcConvertModelViewSet(viewsets.ModelViewSet):
    queryset =  IfcConvertModel.objects.all()
    serializer_class = IfcConvertModelSerializer
    #filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    #filterset_fields = ['projectUUID']
    #permission_classes = (IsAuthenticated,)
    #authentication_class = (TokenAuthentication,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['projectUUID']
        
    def create(self, request, *args, **kwargs):
        # do your customization here
        instance = request.data
        new_post = IfcConvertModel.objects.create(
            projectUUID=instance['projectUUID'], 
            uploadedIfcFileUUID=instance['uploadedIfcFileUUID'], 
            name=instance['name'],
            userU=instance['userU'],
            IFCFile=instance['IFCFile'])
        
        new_post.save()
        serializer = IfcConvertModelSerializer(new_post)
        
        namefile = instance['IFCFile']

        runscript1(namefile)
        file = open(f'{BASE_DIR2}/portal/json_results/temp{namefile}.json', 'r')
        data = json.load(file)
        file.close()
        model_instance = IfcConvertModel.objects.get(id=serializer.data['id'])
        new_json =IfcResultModel.objects.create(IfcFileID=model_instance, IFCjsonResult=data)
        new_json.save()
        from os import remove
        remove(f'{BASE_DIR2}/portal/json_results/temp{namefile}.json')
        return Response({'data':serializer.data, 'json_result': data})

        
class IfcResultModelViewSet(viewsets.ModelViewSet): 
    queryset =  IfcResultModel.objects.all()
    serializer_class = IfcResultSerializer




"""

        import requests
        response = requests.get(f'http://localhost:8000/ConvertIfc/{serializer.data.id}/').json()
        
        file = open(f'{BASE_DIR2}/media/IFCFiles_model/temp_{namefile}', "wb") 
        file.write(response.content)
        
        file.close()        
        
        
        
        
        runscript(namefile)


        file = open(f'{BASE_DIR2}/portal/json_results/{namefile}.json', 'r')
        

        data = json.load(file)


"""