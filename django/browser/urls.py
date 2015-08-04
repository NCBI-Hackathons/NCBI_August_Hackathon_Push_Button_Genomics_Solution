from rest_framework import routers

from django.conf.urls import url, include

import api.views as api_views

router = routers.DefaultRouter()
router.register(r'genes', api_views.GeneViewSet)

urlpatterns = [
    '',
    url(r'api/', include(router.urls), name='browser-api'),
]
