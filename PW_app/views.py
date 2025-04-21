from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages 
from .models import UserProfile , SavedPassword
from cryptography.fernet import Fernet
import base64
import hashlib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .forms import SavedPasswordForm


def generate_fernet_key(masterkey: str) -> bytes:
    key_bytes = masterkey.encode()
    hashed = hashlib.sha256(key_bytes).digest()
    return base64.urlsafe_b64encode(hashed)


def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            messages.success(request,"successfully logged")
            return redirect("dashbord")
        else:
            messages.error(request,"Invalid Crendials")
    return render(request,"login.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        masterkey = request.POST.get("masterkey")
 
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("register")
        
        if username and password and masterkey:
            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, masterkey=masterkey)
            login(request, user)
            messages.success(request, "Welcome")
            return redirect("login")  # should be a string (URL name)
        else:
            return render(request,"register.html")

    return render(request, "register.html")

@login_required(login_url='login')
def add_password(request):
    return render(request, 'add_password.html')

@login_required(login_url='login')
@csrf_exempt
def save_password(request):
    if request.method=="POST":
        site = request.POST.get("site")
        username=request.POST.get("username")
        password = request.POST.get("password")
        
        exits=SavedPassword.objects.filter(
            user=request.user,
            site=site,
            username=username,
        ).exists()
        if exits:
            messages.error(request,"password for this username and website already exits")
            
        else:


            profile,created = UserProfile.objects.get_or_create(user=request.user)
            fernet = Fernet(generate_fernet_key(profile.masterkey)) 
            encrypted_password = fernet.encrypt(password.encode()).decode()

            SavedPassword.objects.create(
                user=request.user,
                site=site,
                username=username,
                password=encrypted_password
            )
            messages.success(request, "Password saved successfully!")
            return redirect("dashbord")
    return render(request,'dashbord.html')

@login_required(login_url='login')
def dashbord(request):
    entries = SavedPassword.objects.filter(user=request.user)

    view_id=request.GET.get('view')
    for entry in entries:
        if view_id and str(entry.id) == view_id:
            profile = UserProfile.objects.get(user=request.user)
            fernet = Fernet(generate_fernet_key(profile.masterkey))
            decrypted = fernet.decrypt(entry.password.encode()).decode()
            entry.decrypted_password = decrypted
        else:
            entry.decrypted_password = None
    return render(request, 'dashbord.html', {'entries': entries})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def home_view(request):
    return render(request,'home.html')


def layout(request):
    return render(request,"layout.html")

@login_required(login_url='login')
def delete_savedpassword(request, password_id):
    password_entry = get_object_or_404(SavedPassword, id=password_id, user=request.user)

    if request.method == "POST":
        
        password_entry.delete()
        return redirect('dashbord')  
    
    return redirect('dashbord')


@login_required
def edit_existing_password(request,password_id):
    entry = get_object_or_404(SavedPassword, id=password_id, user=request.user)

    if request.method=="POST":
        new_password=request.POST.get("password")
        new_website=request.POST.get("Website")

        if new_password:
            entry.password=new_password

        if new_website:
            entry.Website=new_website


        entry.save()
        return redirect('dashbord')
    return render(request, 'edit_existing_password.html', {'entry': entry})
    
    






