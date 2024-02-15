from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from django.core.files.images import ImageFile
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_credential = UserCredential.objects.filter(username=username).first()
        if user_credential and check_password(password, user_credential.password):
            user = user_credential.user_id
            request.session['user_id'] = str(user.user_id)
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

        user_credential = UserCredential.objects.filter(username=username)
        if user_credential.exists():
            messages.error(request, "Username already exists. Please try a different username.")
            return redirect('register')

        # Create the user instance
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.save()

        # Get or create the organization
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
        cred = UserCredential.objects.create(
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
        new_image = UserImage(image=ImageFile(image_file))
        user_id = request.session.get('user_id')
        if user_id is not None:
            user = User.objects.get(user_id=user_id)
            new_image.user = user
            new_image.save()
            messages.success(request, "Image uploaded")
            return redirect('login_page')
        else:
            messages.error(request, "You must be logged in to upload an image.")
    return render(request, 'users_page.html')


def radiologist_view(request):
    # Retrieve all users and their images
    users_with_images = User.objects.filter(images__isnull=False).distinct()

    # Render the radiologist_page.html template with the users and their images
    return render(request, 'radiologist_page.html', {'users_with_images': users_with_images})