from django.db import models

class GstinVerification(models.Model):
    gstin = models.CharField(max_length=15, null=True, blank=True, unique=True)
    gst_certificate = models.CharField(max_length=255, null=True, blank=True)
    pan = models.CharField(max_length=10, null=True, blank=True)
    pan_upload = models.CharField(max_length=255, null=True, blank=True)
    verification_status = models.CharField(max_length=50)
    data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    user_service = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)

    
    # Additional Fields
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_type = models.CharField(max_length=100, null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)

    
    address_line = models.CharField(max_length=255, null=True, blank=True)
    
    license_status = models.CharField(max_length=100, null=True, blank=True)

    director_name = models.CharField(max_length=255, null=True, blank=True)
    director_aadhar_upload = models.CharField(max_length=255, null=True, blank=True)

    iec_number = models.CharField(max_length=20, null=True, blank=True)
    cin_number = models.CharField(max_length=21, null=True, blank=True)
    cin_upload = models.CharField(max_length=255, null=True, blank=True)

    tan_number = models.CharField(max_length=10, null=True, blank=True)
    tan_upload = models.CharField(max_length=255, null=True, blank=True)

    udyam_number = models.CharField(max_length=20, null=True, blank=True)
    udyam_certificate_upload = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "GSTIN_Details"

    def __str__(self):
        return self.gstin


class BankDetails(models.Model):
    contact_person_name = models.CharField(max_length=255, null=True, blank=True)
    contact_person_phone_number = models.CharField(max_length=20, null=True, blank=True)
    address_line_1 = models.CharField(max_length=255, null=True, blank=True)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    user_service = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Bank_Details"

    def __str__(self):
        return f"{self.contact_person_name} - {self.user_id}" if self.contact_person_name else str(self.user_id)


class CommunicationAddress(models.Model):
    contact_person_name = models.CharField(max_length=255, null=True, blank=True)
    contact_person_phone_number = models.CharField(max_length=20, null=True, blank=True)
    address_line_1 = models.CharField(max_length=255, null=True, blank=True)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    address_line_3 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    user_service = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Communication_Address"

    def __str__(self):
        return f"{self.contact_person_name} - {self.user_id}" if self.contact_person_name else str(self.user_id)
