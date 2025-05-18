from django.urls import path
from .views import submit_gstin_details_view

urlpatterns = [
    path('submit-gstin-details/', submit_gstin_details_view, name='submit_tax_details'),
]
