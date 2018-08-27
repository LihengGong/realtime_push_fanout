from rest_framework import viewsets
from .models import PushpinStatConn, PushpinStatSub
from .serializers import PpStatConnSerializer, PpStatSubSerializer


class PushpinStatConnViewSet(viewsets.ModelViewSet):
    """
    viewsets for PushpinStatConn
    """
    queryset = PushpinStatConn.objects.all()
    serializer_class = PpStatConnSerializer


class PushpinStatSubViewSet(viewsets.ModelViewSet):
    """
    viewsets for PushpinStatSub
    """
    queryset = PushpinStatSub.objects.all()
    serializer_class = PpStatSubSerializer
