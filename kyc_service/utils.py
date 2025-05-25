from rest_framework.response import Response
from rest_framework import status as drf_status
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    APIException, AuthenticationFailed, NotAuthenticated, 
    PermissionDenied, ValidationError
)
from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
import logging

# Set up logging for debugging purposes
logger = logging.getLogger(__name__)

def custom_response(data=None, status=200, message=""):
    """
    Standardized API response format for Django REST Framework.

    :param data: The response data (default: None)
    :param status: HTTP status code (default: 200)
    :param message: Custom message (default: empty string)
    :return: Response object in a uniform structure
    """

    # Default response structure

    is_success = status in [200, 201, 202, 203, 204]
    response_payload = { # Renamed to avoid conflict with DRF's Response
        "status": "success" if is_success else "failed",
        "status_code": status,
        "message": message or get_default_message(status),
        "response": data if data is not None else {}
    }

    # Handling error cases
    if status >= 400:
        # Ensure 'errors' key is used consistently for error details
        error_data = data
        if isinstance(data, dict) and 'detail' in data and not isinstance(data['detail'], dict):
             # DRF often puts simple string errors in 'detail'
            error_data = data['detail']
        elif isinstance(data, list): # For multiple validation errors
            error_data = data
        elif data is None:
            error_data = get_default_message(status)


        response_payload["response"] = {"errors": error_data }


    return Response(response_payload, status=status)


def get_default_message(status):
    """
    Returns a default message based on HTTP status code.
    """
    messages = {
        drf_status.HTTP_200_OK: "Request successful.",
        drf_status.HTTP_201_CREATED: "Resource created successfully.",
        drf_status.HTTP_204_NO_CONTENT: "Request successful with no content to return.",
        drf_status.HTTP_400_BAD_REQUEST: "Bad request. Please check your input.",
        drf_status.HTTP_401_UNAUTHORIZED: "Authentication required.",
        drf_status.HTTP_403_FORBIDDEN: "Access denied.",
        drf_status.HTTP_404_NOT_FOUND: "Requested resource not found.",
        drf_status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal server error. Try again later.",
    }
    return messages.get(status, "An unexpected error occurred.")


def custom_exception_handler(exc, context):
    """Handles all exceptions globally and returns a standardized custom response."""
    
    # First, let DRF handle its built-in exceptions to get the initial response
    response = exception_handler(exc, context)

    # Extract useful information for debugging
    error_message = str(exc)
    view_name = context['view'].__class__.__name__ if 'view' in context else 'UnknownView'
    request_path = context['request'].path if 'request' in context else 'UnknownPath'
    
    logger.error(f"Exception in {view_name} at {request_path}: {error_message}", exc_info=True) # Added exc_info for full traceback

    if response is not None:
        # We are using DRF's response, let's re-wrap it with custom_response
        # Extract original data and status
        original_data = response.data
        original_status = response.status_code
        
        # Specific DRF exception messages
        if isinstance(exc, NotAuthenticated):
            return custom_response(data=original_data, status=original_status, message="Missing authentication token.")
        elif isinstance(exc, AuthenticationFailed):
            return custom_response(data=original_data, status=original_status, message="Token is invalid or expired.")
        elif isinstance(exc, PermissionDenied):
            return custom_response(data=original_data, status=original_status, message="You do not have permission to perform this action.")
        elif isinstance(exc, ValidationError):
            # For ValidationError, exc.detail often contains the structured error messages
            return custom_response(data=exc.detail, status=original_status, message="Validation failed.")
        else: # For other DRF APIExceptions
            message = original_data.get('detail', get_default_message(original_status)) if isinstance(original_data, dict) else get_default_message(original_status)
            return custom_response(data=original_data, status=original_status, message=str(message))

    else:
        # Handle non-DRF exceptions (database errors, unexpected errors)
        if isinstance(exc, DatabaseError):
            return custom_response(data=None, status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR, message="A database error occurred. Please contact support.")
        if isinstance(exc, ObjectDoesNotExist):
            return custom_response(data=None, status=drf_status.HTTP_404_NOT_FOUND, message="The requested resource was not found.")

        # Handle any other unhandled Python exceptions
        return custom_response(data=None, status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected server error occurred. Please try again later.")

    # This line should ideally not be reached if all paths return a custom_response
    # but as a fallback, return the original DRF response if it exists
    return response
