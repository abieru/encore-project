from django.views.generic.base import TemplateView  
from django.views.generic.edit import CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import resolve, reverse_lazy
from .getData import *
from .models import IFCFilejson, IfcConvertModel, IfcConvertModel
from django.utils.safestring import SafeString
import json
from django.views.generic.list import ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import IfcConvertModelSerializer,  IfcConvertModelSerializer
from rest_framework.parsers import FileUploadParser

@method_decorator(login_required, name="dispatch")
class PortalClassView(TemplateView):

    template_name = "portal/portal.html" 

    def get_context_data(self, **kwargs):
        data_project = obtenerdataEngeneral()
        context = super().get_context_data(**kwargs)
        context['projects'] = data_project
        return context
        

@method_decorator(login_required, name="dispatch")
class PortalcreateView(CreateView):
    
    
    model = IFCFilejson
    fields =['uploadedIfcFileUUID', 'projectUUID', 'description', 'name', 'userU', 'IFCjson', 'dateAndTime']
    template_name = "portal/portaldetail.html" 


    def get_context_data(self, **kwargs):
        dataofprojecto = getoneProject(self.kwargs.get('slug'))
        archivos = getifcfile(self.kwargs.get('slug'))
        dataifc = getifcinfo(self.kwargs.get('slug'))
        context = super().get_context_data(**kwargs)
        context['project'] = dataofprojecto

        context['files_url'] = archivos#json.dumps(archivos)

        context['ifcdata'] =  dataifc

        return context  
	
    
    def get_success_url(self):
		
        return reverse_lazy('home') + '?projectcreate'

@method_decorator(login_required, name="dispatch")    
class PortalListView(ListView):
    model = IFCFilejson
    template_name = 'portal/resultjson.html'



@method_decorator(login_required, name="dispatch")
class ProjectDelete(DeleteView):
    model = IFCFilejson 
    template_name = 'portal/page_confirm_delete.html'
    def get_success_url(self):
		
        return reverse_lazy('home') + '?projectdelete'


"""


class IfcConvertModelView(APIView):
    parser_class = [FileUploadParser]

    def get(self, request):
        articles = IfcConvertModel.objects.all()
        
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = IfcConvertModelSerializer(articles, many=True)
        return Response({"IfcConvert": serializer.data})


    def post(self, request,filename, format=None):    
        article = request.data.get('IfcConvert')
        file_obj = request.FILES['file']
        # Create an article from the above data
        IfcConvertModel.IFCFile.save(file_obj.name, file_obj, save=True)
        serializer = IfcConvertModelSerializer(data=[article,file_obj])
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({"success": f"Json data: {article_saved.title} created successfully, id: {article_saved.id}"})





"""














"""
class FileUploadView(APIView):
    parser_classes = (FileUploadParser, )

    def post(self, request, format='jpg'):
        up_file = request.FILES['file']
        destination = open('/Users/Username/' + up_file.name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        destination.close()  # File should be closed only after all chuns are added

        # ...
        # do some stuff with uploaded file
        # ...
        return Response(up_file.name, status.HTTP_201_CREATED)

"""
