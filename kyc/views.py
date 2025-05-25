from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import GstinVerification
from .serializers import GstinVerificationSerializer
from .utils import fetch_gstin_detailed # Import the function
import requests # requests is already imported, but ensure it's available if not.
import os
import json

@api_view(['POST'])
def submit_gstin_or_pan_view(request):
    serializer = GstinVerificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        gstin_details = fetch_gstin_detailed_details()
        
        return Response(gstin_details, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
