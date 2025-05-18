from django.urls import path
from .views import verify_gstin_view

urlpatterns = [
    path('verify-gstin/', verify_gstin_view, name='verify_gstin'),
]
