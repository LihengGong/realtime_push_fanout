from rest_framework import serializers
from .models import PushpinStat_Conn, PushpinStat_Sub


class ppStatConnSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushpinStat_Conn
        fields = '__all__'


class ppStatSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushpinStat_Sub
        fields = '__all__'
