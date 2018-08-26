from rest_framework import serializers
from .models import PushpinStatConn, PushpinStatSub


class PpStatConnSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushpinStatConn
        fields = '__all__'


class PpStatSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushpinStatSub
        fields = '__all__'
