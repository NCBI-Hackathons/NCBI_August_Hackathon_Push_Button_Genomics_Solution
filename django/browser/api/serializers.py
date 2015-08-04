from rest_framework import serializers as drf_serialiazers

from browser.models import Gene

class GeneSerializer(drf_serialiazers.ModelSerializer):
    """
    `Gene` serializer.
    """
    class Meta:
        model = Gene
