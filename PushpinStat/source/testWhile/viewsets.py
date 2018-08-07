from rest_framework import viewsets
from .models import PushpinStat_Conn, PushpinStat_Sub
from .serializers import ppStatConnSerializer, ppStatSubSerializer


class PushpinStatConnViewSet(viewsets.ModelViewSet):
    queryset = PushpinStat_Conn.objects.all()
    serializer_class = ppStatConnSerializer


class PushpinStatSubViewSet(viewsets.ModelViewSet):
    queryset = PushpinStat_Sub.objects.all()
    serializer_class = ppStatSubSerializer
