from rest_framework import viewsets as drf_viewsets

from browser.models import Gene

from .serializers import GeneSerializer

class GeneViewSet(drf_viewsets.ModelViewSet):
    """
    API endpoint that allows runs to be viewed and edited.
    """
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer
