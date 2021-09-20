from rest_framework import routers
from .viewsets import PortalViewSet

router =routers.SimpleRouter()
router.register('projects', PortalViewSet )

urlpatterns= router.urls
from django.urls import path
#from .views import PortalClassView, PortalcreateView
"""
urlpatterns = [
    path('', PortalClassView.as_view(), name="home"),
    path('<slug:slug>/detail/', PortalcreateView.as_view(), name="detail_project"),

]


"""

 