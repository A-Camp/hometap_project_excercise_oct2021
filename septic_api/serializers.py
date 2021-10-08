# serializers.py
from rest_framework import serializers
from .models import Home
from . import houseCanary_api

class HomeSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    id = serializers.ReadOnlyField

    def create(self, validated_data):
        has_septic = houseCanary_api.get_septic(validated_data)
        data = {**validated_data, 'has_septic': has_septic }
        return Home.objects.create(**data)

    class Meta:
        model = Home
        fields = ('id', 'address', 'zipcode', 'city', 'state', 'owner', 'has_septic', 'user_septic_info')