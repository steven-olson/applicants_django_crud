from django.db import models
import uuid


class Applicant(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=30, blank=False, editable=False)
    last_name = models.CharField(max_length=30, blank=False, editable=False)
    email_address = models.CharField(max_length=500, blank=False, editable=False)
    phone_number = models.CharField(max_length=20, blank=False, editable=False)
    note = models.CharField(max_length=500, blank=True, null=True, editable=True)
    approval_status = models.BooleanField(default=False, editable=True)

    class Meta:
        permissions = [
            ("can_view_applicant", "Can view existing applicants"),
            ("can_create_applicant", "Can create new applicants"),
            ("can_accept_reject_applicant", "Can edit `approval_status` field on an applicant"),
            ("can_create_update_note", "Can update `note` field on an applicant")
        ]
