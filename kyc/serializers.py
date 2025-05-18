from rest_framework import serializers
from .models import GstinVerification

class GstinVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GstinVerification
        fields = '__all__'
