from django.urls import path
from .views import submit_gstin_or_pan_view

urlpatterns = [
    path('submit-gstin-or-pan/', submit_gstin_or_pan_view, name='submit_gstin_or_pan'),
]
