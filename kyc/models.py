from django.db import models

class GstinVerification(models.Model):
    gstin = models.CharField(max_length=15, unique=True)
    verification_status = models.CharField(max_length=50)
    data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    pan = models.CharField(max_length=10, null=True, blank=True)
    user_service = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "GSTIN_Details"

    def __str__(self):
        return self.gstin
