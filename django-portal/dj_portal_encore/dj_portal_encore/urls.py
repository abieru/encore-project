
from django.contrib import admin
from django.urls import path, include
from portal.views import PortalClassView, PortalcreateView, PortalListView, ProjectDelete
from django.conf import settings
from rest_framework.authtoken import views

from django.conf.urls.static import static
urlpatterns = [
    path('', include('portal.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),

    #api
    path('api/v1.0/', include('portal.urls')),

    path('admin1/', admin.site.urls),
    path('', PortalClassView.as_view(), name="home"),

    #path('projectupload/', IfcConvertModelView.as_view(), name="projectuploadlist"),

    path('apilist/', PortalListView.as_view(), name="listview"),
    path('<slug:slug>/detail/', PortalcreateView.as_view(), name="detail_project"),
    path('delete/<int:pk>/', ProjectDelete.as_view(), name='deleteP'),

    path('generatetoken/', views.obtain_auth_token),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)