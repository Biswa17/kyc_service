from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import GstinVerification
from .serializers import GstinVerificationSerializer
import requests
import os
import json

@api_view(['POST'])
def verify_gstin_view(request):
    try:
        data = json.loads(request.body)
        gstin = data.get('gstin')
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)

    if not gstin:
        return Response({"error": "GSTIN is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if GSTIN is already verified
    try:
        verification = GstinVerification.objects.get(gstin=gstin)
        serializer = GstinVerificationSerializer(verification)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except GstinVerification.DoesNotExist:
        pass

        # # Implement Gridlines API integration here
        # api_key = os.environ.get('GRIDLINES_API_KEY')
        # url = "https://gridlines.stoplight.io/docs/gridlines-api-docs/397f3ea345b13-fetch-gstin-lite" # Replace with actual API endpoint
        # headers = {"Authorization": f"Bearer {api_key}"}
        # try:
        #     response = requests.get(f"{url}?gstin={gstin}", headers=headers)
        #     response.raise_for_status()
        #     data = response.json()
        #     verification_status = "Verified" # Determine status from API response
        #     verification = GstinVerification.objects.create(
        #         gstin=gstin,
        #         verification_status=verification_status,
        #         data=data
        #     )
        #     serializer = GstinVerificationSerializer(verification)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # except requests.exceptions.RequestException as e:
        #     return Response({"error": f"API error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # except Exception as e:
        #     return Response({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
