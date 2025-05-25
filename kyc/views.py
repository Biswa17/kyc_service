from django.http import JsonResponse 
from rest_framework.decorators import api_view
from rest_framework import status as drf_status
from .models import GstinVerification
from .serializers import GstinVerificationSerializer
from django.db import utils as db_utils 
from kyc_service.utils import custom_response
from .utils import fetch_gstin_detailed, fetch_gstin_by_pan # Updated import names

@api_view(['POST'])
def submit_gstin_or_pan_view(request):
    serializer = GstinVerificationSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save() # Save and get the instance

        gstin_provided = serializer.validated_data.get('gstin')
        pan_provided = serializer.validated_data.get('pan')
        external_api_data = None

        if gstin_provided:
            print(f"Fetching detailed GSTIN info for: {gstin_provided}")
            external_api_data = fetch_gstin_detailed(gstin_number=gstin_provided) # Updated function call
        elif pan_provided: # Only if GSTIN was not provided
            print(f"Fetching GSTIN info by PAN: {pan_provided}")
            external_api_data = fetch_gstin_by_pan(pan_number=pan_provided) # Updated function call
        
        if external_api_data:
            instance.data = external_api_data
            instance.save(update_fields=['data']) # Save only the updated 'data' field
            print("External API data saved to instance.")
            # Re-serialize the instance to include the updated 'data' in the response
            response_serializer = GstinVerificationSerializer(instance)
            return custom_response(
                data=response_serializer.data,
                status=drf_status.HTTP_201_CREATED
            )
        else:
            # If no external call was made or it failed, return the original instance data
            print("No external API call made or call failed. Returning initial data.")
            return custom_response(
                data=serializer.data, # This is data before external call update
                status=drf_status.HTTP_201_CREATED
            )
    
    return custom_response(
        data=serializer.errors, 
        status=drf_status.HTTP_400_BAD_REQUEST, 
        message="Validation failed. Please check your input."
    )
