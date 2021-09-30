from django.views.generic.base import TemplateView  
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import resolve, reverse_lazy
from .getData import *
from .models import IFCFilejson
from django.utils.safestring import SafeString
import json


@method_decorator(login_required, name="dispatch")
class PortalClassView(TemplateView):

    template_name = "portal/portal.html" 

    def get_context_data(self, **kwargs):
        data_project = response_f
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

    


