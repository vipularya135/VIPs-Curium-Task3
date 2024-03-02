from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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
                return redirect('surgeon_view')
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
        org_name = request.POST.get('org_name')

        user_credential = UserCredential.objects.filter(username=username)
        if user_credential.exists():
            messages.error(request, "Username already exists. Please try a different username.")
            return redirect('register')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.save()

        orgg, created = Organization.objects.get_or_create(
            org_name=org_name,
            defaults={
                'org_owner': user,
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
        user_id = request.session.get('user_id')
        if user_id is not None:
            user = User.objects.get(user_id=user_id)
            image_name = default_storage.save('user_images/' + image_file.name, image_file)
            image_url = default_storage.url(image_name)
            org = Organization.objects.get(org_owner=user)
            volume_meta_data = {"volume_path": image_url}
            volume_record = VolumeRecord(uploaded_by=user, org_id=org, volume_meta=volume_meta_data)
            volume_record.save()
            messages.success(request, "Image uploaded")
            return redirect('login_page')
        else:
            messages.error(request, "You must be logged in to upload an image.")
    else:
        user_id = request.session.get('user_id')
        if user_id is not None:
            user = User.objects.get(user_id=user_id)
            user_credential = UserCredential.objects.get(user_id=user)
            context = {
                'user': user,
                'username': user_credential.username,
            }
            return render(request, 'users_page.html', context)
    


@csrf_exempt
def radiologist_view(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        user = User.objects.get(user_id=user_id)
        user_credential = UserCredential.objects.get(user_id=user)
        user_org = Membership.objects.get(user_id=user).org_id
        users_with_records = User.objects.filter(membership__org_id=user_org, volumerecord__isnull=False).distinct()

        if request.method == 'POST':
            record_id = request.POST.get('record_id')
            record = VolumeRecord.objects.get(record_id=record_id)
            if record.status != VolumeRecord.Status.COMPLETED:
                record.status = VolumeRecord.Status.COMPLETED
                record.save()
                return JsonResponse({'status': 'success'})

        context = {
            'users_with_records': users_with_records,
            'username': user_credential.username,
        }
    else:
        context = {
            'users_with_records': [],
        }
    return render(request, 'radiologist_page.html', context)



def surgeon_view(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        user = User.objects.get(user_id=user_id)
        user_credential = UserCredential.objects.get(user_id=user)
        user_org = Membership.objects.get(user_id=user).org_id 
        users_with_records = User.objects.filter(membership__org_id=user_org, volumerecord__status=VolumeRecord.Status.COMPLETED).distinct()
        records = {user: user.volumerecord_set.filter(status=VolumeRecord.Status.COMPLETED) for user in users_with_records}
        context = {
            'records': records,
            'username': user_credential.username,
        }
    else:
        context = {
            'records': {},
        }
    return render(request, 'surgeon_page.html', context)
