from django.db import models
from uuid import uuid4
from django.core.files.images import ImageFile
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_column='user_id')
    first_name = models.CharField(max_length=255, db_column='first_name')
    last_name = models.CharField(max_length=255, db_column='last_name')
    email = models.EmailField(unique=True, db_column='email')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'app_user'

class Organization(models.Model):
    org_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_column='org_id')
    org_owner = models.ForeignKey(User, on_delete=models.CASCADE, db_column='org_owner_id')
    org_name = models.CharField(max_length=255, db_column='org_name')
    org_description = models.TextField(db_column='org_description')
    org_address = models.TextField(db_column='org_address')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'app_organization'

class Membership(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN'
        SURGEON = 'SURGEON'
        TELERADIOLOGIST = 'TELERADIOLOGIST'

    membership_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_column='membership_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE, db_column='org_id')
    role_name = models.CharField(max_length=20, choices=Role.choices, default=Role.ADMIN, db_column='role_name')

    class Meta:
        db_table = 'app_membership'

class UserCredential(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, db_column='user_id')
    username = models.CharField(max_length=255, db_column='username')
    password = models.CharField(max_length=255, db_column='password')

    class Meta:
        db_table = 'app_user_credential'

class VolumeRecord(models.Model):
    class Status(models.TextChoices):
        UPLOADED = 'UPLOADED'
        QUEUED = 'QUEUED'
        PROCESSING = 'PROCESSING'
        INTERMEDIATE_STATE = 'INTERMEDIATE_STATE'
        COMPLETED = 'COMPLETED'

    record_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_column='record_id')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uploaded_by_id')
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE, db_column='org_id')
    upload_date = models.DateTimeField(auto_now_add=True, db_column='upload_date')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADED, db_column='status')
    patient_id = models.CharField(max_length=255, db_column='patient_id')
    study_id = models.CharField(max_length=255, db_column='study_id')
    isAutomated = models.BooleanField(default=False, db_column='is_automated')

    class Meta:
        db_table = 'app_volume_record'

class UserImage(models.Model):
    image_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_column='image_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images', db_column='user_id')
    image = models.ImageField(upload_to='user_images/', db_column='image')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'app_user_image'
