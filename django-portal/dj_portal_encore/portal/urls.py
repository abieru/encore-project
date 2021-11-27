from rest_framework import routers
from .viewsets import IfcConvertModelViewSet, PortalViewSet, IfcResultModelViewSet

router =routers.SimpleRouter()
router.register('projects', PortalViewSet )

router.register('ConvertIfc', IfcConvertModelViewSet )
router.register('Project_result_json', IfcResultModelViewSet )


urlpatterns= router.urls
from django.urls import path
#from .views import PortalClassView, PortalcreateView

"""

urlpatterns = [

    path('', PortalClassView.as_view(), name="home"),
    path('<slug:slug>/detail/', PortalcreateView.as_view(), name="detail_project"),

]

"""
