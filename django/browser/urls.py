from rest_framework import routers

from django.conf.urls import url, include, patterns

import api.views as api_views
import views as html_views

router = routers.DefaultRouter()
router.register(r'genes', api_views.GeneViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls), name='browser-api'),
    url('', html_views.IndexView.as_view(), name='index'),
)
