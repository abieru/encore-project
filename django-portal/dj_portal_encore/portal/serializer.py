from rest_framework import serializers
from .models import IFCFilejson

class PortalSerializer(serializers.ModelSerializer):
    class Meta:
        model= IFCFilejson
        fields ='__all__'
        