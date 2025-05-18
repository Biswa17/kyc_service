from django.db import models

class GstinVerification(models.Model):
    gstin = models.CharField(max_length=15, unique=True)
    verification_status = models.CharField(max_length=50)
    data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.gstin
