from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from django.core.files.images import ImageFile
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist



def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = str(user.user.id)
            current_user = user
            wow = Membership.objects.filter(user_id=current_user).last()
            if wow.role_name == 'user':
                return redirect('user_view')
            elif wow.role_name == 'surgeon':
                return redirect('surgeons_view')
            elif wow.role_name == 'radiologist':
                return redirect('radiologist_view')
        messages.error(request, "Invalid username or password.")    
    return render(request, 'login.html')



def logout_page(request):
    logout(request)
    return redirect('login_page')



def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role_name = request.POST.get('role_name')

        if User.objects.filter(username == username).exists():
            messages.error(request, "Username already exists. Please try a different username.")
            return redirect('register')


        user = User.objects.create_user(username = username, email = email, role_name = role_name, first_name = first_name, last_name = last_name)
        user.save()

        org_name = 'Test Organisation'
        orgg, created = Organization.objects.get_or_create(
            org_name=org_name,
            defaults={
                'org_owner': user,  # Set the actual user who owns the organization
                'org_description': 'Test Description',
                'org_address': 'Test Address'
            }
        )

        hashed_password = make_password(password)
        cred = User.objects.create(
            user_id=user,
            username=username,
            password=hashed_password
        )
        cred.save()

        mem = Membership.objects.create(
            user_id=user,
            role_name=role_name,
            org_id=orgg
        )
        mem.save()

        messages.success(request, "Account created successfully.")
        return redirect('login_page')
    return render(request, 'register.html')



def user_view(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        user_id = request.session.get('user_id')
        if user_id is not None:
            user = User.objects.get(user_id=user_id)
            image_name = default_storage.save('user_images/' + image_file.name, image_file)
            image_url = default_storage.url(image_name)
            org = Organization.objects.get(org_owner=user)
            volume_record = VolumeRecord(uploaded_by=user, org_id=org, volume_meta=image_url)
            volume_record.save()
            messages.success(request, "Image uploaded")
            return redirect('login_page')
        else:
            messages.error(request, "You must be logged in to upload an image.")
    else:
        user_id = request.session.get('user_id')
        if user_id is not None:
            user = User.objects.get(user_id=user_id)
            user_credential = User.objects.get(user_id=user)
            context = {
                'user': user,
                'username': user_credential.username,
            }
            return render(request, 'users_page.html', context)
    


def radiologist_view(request):
    # Retrieve all users and their VolumeRecords
    users_with_records = User.objects.filter(volumerecord__isnull=False).distinct()

    user_id = request.session.get('user_id')
    if user_id is not None:
        user = User.objects.get(user_id=user_id)
        user_credential = User.objects.get(user_id=user)
        context = {
            'users_with_records': users_with_records,
            'username': user_credential.username,
        }
    else:
        context = {
            'users_with_records': users_with_records,
        }

    # Render the radiologist_page.html template with the users and their VolumeRecords
    return render(request, 'radiologist_page.html', context)