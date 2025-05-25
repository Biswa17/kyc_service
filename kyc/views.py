from django.http import JsonResponse 
from rest_framework.decorators import api_view
from rest_framework import status as drf_status
from .models import GstinVerification
from .serializers import GstinVerificationSerializer
from django.db import utils as db_utils 
from kyc_service.utils import custom_response

@api_view(['POST'])
def submit_gstin_or_pan_view(request):
    serializer = GstinVerificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(
            data=serializer.data, 
            status=drf_status.HTTP_201_CREATED
        )
    
    return custom_response(
        data=serializer.errors, 
        status=drf_status.HTTP_400_BAD_REQUEST, 
        message="Validation failed. Please check your input."
    )
