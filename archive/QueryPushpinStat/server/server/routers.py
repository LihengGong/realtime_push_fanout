from rest_framework import routers
from testWhile.viewsets import PushpinStatConnViewSet, PushpinStatSubViewSet


router = routers.DefaultRouter()

router.register(r'statconn', PushpinStatConnViewSet)
router.register(r'statsub', PushpinStatSubViewSet)
