from rest_framework import serializers
from .models import GstinVerification

class GstinVerificationSerializer(serializers.ModelSerializer):
    gstin = serializers.CharField(max_length=15, required=False, allow_null=True, allow_blank=True)
    pan = serializers.CharField(max_length=10, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = GstinVerification
        fields = ['id', 'gstin', 'pan', 'verification_status', 'data', 'created_at', 'updated_at', 'user_service', 'user_id']
        read_only_fields = ['id', 'verification_status', 'data', 'created_at', 'updated_at']

    def validate(self, data):
        gstin = data.get('gstin')
        pan = data.get('pan')

        if not gstin and not pan:
            raise serializers.ValidationError("Either GSTIN or PAN must be provided.")

        return data
