from django.db import models
from uuid import uuid4

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_user'

class Organization(models.Model):
    org_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    org_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=255)
    org_description = models.TextField()
    org_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_organization'

class Membership(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN'
        SURGEON = 'SURGEON'
        TELERADIOLOGIST = 'TELERADIOLOGIST'

    membership_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=20, choices=Role.choices, default=Role.ADMIN)

    class Meta:
        db_table = 'app_membership'

class UserCredential(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'app_user_credential'

class VolumeRecord(models.Model):
    class Status(models.TextChoices):
        UPLOADED = 'UPLOADED'
        QUEUED = 'QUEUED'
        PROCESSING = 'PROCESSING'
        INTERMEDIATE_STATE = 'INTERMEDIATE_STATE'
        COMPLETED = 'COMPLETED'

    record_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADED)
    patient_id = models.CharField(max_length=255)
    study_id = models.CharField(max_length=255)
    isAutomated = models.BooleanField(default=False)

    class Meta:
        db_table = 'app_volume_record'

class UserImage(models.Model):
    image_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='user_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_user_image'
