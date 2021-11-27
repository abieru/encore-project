from rest_framework import serializers
from .models import IFCFilejson, IfcConvertModel, IfcResultModel

class PortalSerializer(serializers.ModelSerializer):
    class Meta:
        model= IFCFilejson
        fields ='__all__'




class IfcConvertModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= IfcConvertModel
        fields ='__all__'
    


class IfcResultSerializer(serializers.ModelSerializer):
    class Meta:
        model= IfcResultModel
        fields ='__all__'


