from rest_framework import serializers

from location.models import Location

class LocationSerializer(serializers.ModelSerializer):
    city = serializers.CharField()
    class Meta:
        model = Location
        fields = ('cp','city')