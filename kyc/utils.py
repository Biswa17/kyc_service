import requests
import json
import os

def make_api_request(method, url, headers=None, json_data=None, data=None, params=None, timeout=10):
    """
    A generic function to make API requests.
    """
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=json_data, # Use this for application/json content type
            data=data,       # Use this for form-encoded data
            params=params,   # For URL query parameters
            timeout=timeout
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        return response.json()  # Assumes JSON response, adjust if needed
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh} - Response: {errh.response.text if errh.response else 'No response text'}")
        # You might want to return errh.response or parts of it
        return None # Or raise a custom exception
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return None # Or raise
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return None # Or raise
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
        return None # Or raise
    except json.JSONDecodeError as errj: # If response.json() fails
        print(f"JSON Decode Error: {errj} - Response text: {response.text if 'response' in locals() and hasattr(response, 'text') else 'N/A'}")
        return None # Or raise

def fetch_gstin_detailed(gstin_number="21AAXXXXXXXXXXX", consent="Y"):
    """
    Fetches detailed GSTIN details from the external API.
    """
    api_url = "https://stoplight.io/mocks/gridlines/gridlines-api-docs/133154717/gstin-api/fetch-detailed"  # Updated URL
    api_key = "123"  # Default API key from cURL example

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Prefer": "code=200",  # Updated Prefer header
        "X-API-Key": api_key,
        "X-Auth-Type": "API-Key",
        "X-Reference-ID": "" # You might want to generate a unique reference ID here if needed
    }
    # gstin_number will use its default from the function signature if not provided.
    # consent also has a default in the function signature.
    payload = {
        "gstin": gstin_number,
        "consent": consent
    }

    return make_api_request(method="POST", url=api_url, headers=headers, json_data=payload)

def fetch_gstin_by_pan(pan_number="AAAXXXXXXX", consent="Y"):
    """
    Fetches GSTIN details by PAN from the external API.
    """
    api_url = "https://stoplight.io/mocks/gridlines/gridlines-api-docs/133154717/gstin-api/fetch-by-pan"
    api_key = "123" # Default API key from cURL example

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Prefer": "code=200",
        "X-API-Key": api_key,
        "X-Auth-Type": "API-Key",
        "X-Reference-ID": "" 
    }
    payload = {
        "pan_number": pan_number,
        "consent": consent
    }

    return make_api_request(method="POST", url=api_url, headers=headers, json_data=payload)
