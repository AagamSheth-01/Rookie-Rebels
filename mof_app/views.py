from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Usr_prof
from datetime import datetime
from .models import Movie

# Create your views here.
def reg(request):
    if request.method == "POST":
        full_name = request.POST.get("name")  # Match 'name' from form
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        role = request.POST.get("role")  # Change "Role" to lowercase 
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not full_name or not email or not phone or not  role:
            return HttpResponse("Error: Some fields are missing!")
        if password != confirm_password:
            return HttpResponse("Error: Passwords do not match!")
        if Usr_prof.objects.filter(email=email).exists():
            return HttpResponse("Error: Email already in use!")

        print(f"Received: {full_name}, {email}, {phone}, {role}")  # Debugging
        hashed_password = make_password(password)

        # Save to the database (Ensure you have a UserProfile model)
        user = Usr_prof(full_name=full_name, email=email, phone=phone, role=role, password=hashed_password)
        user.save()

        subject = "Verify Your Email"
        message = f"Hi {full_name},\n\nThank you for registering! Please verify your email by clicking the link below:\n\nhttp://127.0.0.1:8000/verify/{user.id}/"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print(f"Email Error: {e}")  # Debugging

        return HttpResponse("Registration successful! Please check your email for verification.")


       
        return redirect('login')  # Redirect after successful registration

    return render(request, "registration/usr_reg.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Debugging: Check if email and password are received correctly
        print(f"Login Attempt: Email={email}, Password={password}")

        user = Usr_prof.objects.filter(email=email).first()

        if user and check_password(password, user.password):  # Verify hashed password
            request.session['user_id'] = user.id  # Manually set session
            messages.success(request, "Login successful!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'registration/login.html')

      
def logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")

def verify_email(request, user_id):
    try:
        user = Usr_prof.objects.get(id=user_id)
        user.is_active = True  # Activate user after verification
        user.save()
        return  redirect("login")
    except Usr_prof.DoesNotExist:
        return HttpResponse("Invalid verification link!")
    
def dashboard(request):
    movies = Movie.objects.all()
    return render(request, 'app/dashboard.html', {'movies': movies}) 


def add_movie(request):
    if request.method == "POST":
        name = request.POST.get("movieName")
        director = request.POST.get("director")
        budget = request.POST.get("budget")
        image_url = request.POST.get("imageUrl")
        
        if not name or not director or not budget or not image_url:
            messages.error(request, "Please fill in all fields!")
            return redirect("add_movie")
        
        Movie.objects.create(name=name, director=director, budget=budget, image_url=image_url)
        messages.success(request, "Movie added successfully!")
        return redirect("dashboard")
    
    return render(request, 'app/add_movies.html')


def delete_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.delete()
    messages.success(request, "Movie deleted successfully!")
    return redirect("dashboard")

# Home view
def home(request):
    username = request.session.get('username', 'Guest')
    current_time = datetime.now()
    notifications = ["New movie releases coming soon!", "Special discount on movie tickets!"]
    
    return render(request, 'app/home.html', {
        'username': username,
        'current_time': current_time,
        'notifications': notifications
    })
