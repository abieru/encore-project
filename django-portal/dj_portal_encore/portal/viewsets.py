from rest_framework import viewsets
from .models import IFCFilejson
from .serializer import PortalSerializer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import mimetypes
mimetypes.add_type("text/css", ".css", True)

#@method_decorator(login_required, name="dispatch")
class PortalViewSet(viewsets.ModelViewSet):
    queryset =  IFCFilejson.objects.all()
    serializer_class = PortalSerializer