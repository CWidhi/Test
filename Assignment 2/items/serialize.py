from rest_framework import serializers
from .models import Items

class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        exclude = ['created_at', 'updated_at', 'id', 'is_deleted']