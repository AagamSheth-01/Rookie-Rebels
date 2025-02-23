from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Usr_prof
from datetime import datetime
from .models import Movie
from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required 
import matplotlib

matplotlib.use('Agg')  
import io
import urllib
import base64
import matplotlib.pyplot as plt

from django.shortcuts import render
from .models import Movie


def budget_comparison(request):
    movies = Movie.objects.all()

    # Extract data
    movie_names = [movie.name for movie in movies]
    budgets = [movie.budget for movie in movies]

    # Plot the graph
    plt.figure(figsize=(10, 5))
    plt.bar(movie_names, budgets, color='skyblue')
    plt.xlabel('Movies')
    plt.ylabel('Budget (in currency)')
    plt.title('Movie Budget Comparison')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a string buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image to base64
    graph = base64.b64encode(image_png).decode('utf-8')
    plt.close()

    return render(request, 'app/budget_comparison.html', {'graph': graph})


# Create your views here.


def reg(request):
    if request.method == "POST":
        full_name = request.POST.get("name")  # Match 'name' from form
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        role = request.POST.get("role")  # Change "Role" to lowercase 
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if Usr_prof.objects.filter(email=email).exists():
            messages.error(request, "Error: Email already in use!")
            return redirect("reg")  # Prevent duplicate entry

        if not full_name or not email or not phone or not  role:
            messages.error(request, "All fields are required!")
            return redirect("reg")
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("reg")
            
        if Usr_prof.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return redirect("reg")

        print(f"Received: {full_name}, {email}, {phone}, {role}")  # Debugging
        hashed_password = make_password(password)

        is_staff_status = role == "Admin"
        is_superuser_status = role == "Admin"

        user = Usr_prof(
            full_name=full_name,
            email=email,
            phone=phone,
            role=role,
            password=hashed_password,
            is_staff=is_staff_status,
            is_superuser=is_superuser_status,
        )
        user.save()

        is_staff_status = True if role == 'Admin' else False 
        # Generate a verification token
        
        user = Usr_prof(full_name=full_name, email=email, phone=phone, role=role, password=hashed_password, is_staff=is_staff_status)
        user.save()

       
      
        

        
        
        
       
        return redirect('login')  # Redirect after successful registration

    return render(request, "registration/usr_reg.html")

def login(request):
    next_url = request.GET.get('next', 'dashboard')  # Default to 'dashboard' if 'next' is not provided

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Debugging: Check if email and password are received correctly
        print(f"Login Attempt: Email={email}, Password={password}")

        user = Usr_prof.objects.filter(email=email).first()

        if user and check_password(password, user.password):  # Verify hashed password
            auth_login(request, user)  # Manually set session
            messages.success(request, "Login successful!")
            return redirect(next_url)  # ✅ Correct redirect

        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'registration/login.html', {"next": next_url})  # ✅ Removed unreachable code


      
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")




def dashboard(request):
    movies = Movie.objects.all()  # Fetch movies (modify as needed)
    
    # Ensure the template knows if the user is an admin
    return render(request, 'app/dashboard.html', {
        'movies': movies,
        'is_admin': request.user.role == 'Admin'  # Check role
    })


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


def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, 'app/redi.html', {'movie': movie})

from django.shortcuts import render, get_object_or_404

def edit_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, 'edit_movie.html', {'movie': movie})
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required





def movie_dashboard(request):
    return render(request, "app/dashboard.html", {"user_role": request.user.role})

@login_required
def profile(request):
    return render(request, 'registration/profile.html')



def budget_comparison(request):
    movies = Movie.objects.all()

    if not movies.exists():
        return render(request, "app/budget_comparison.html", {
            "chart1": None,
            "chart2": None,
            "movies": []
        })

    movie_names = [movie.name for movie in movies]
    budgets = [float(movie.budget) for movie in movies]

    if not movie_names or not budgets:
        return render(request, "app/budget_comparison.html", {
            "chart1": None,
            "chart2": None,
            "movies": movies
        })

    # Function to encode Matplotlib images
    def encode_plot():
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()
        return image

    # Generate Bar Chart
    plt.figure(figsize=(10, 5))
    plt.bar(movie_names, budgets, color='skyblue')
    plt.xlabel('Movies')
    plt.ylabel('Budget (₹ Crores)')
    plt.title('Movie Budget Comparison')
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart1 = encode_plot()

    # Generate Pie Chart
    plt.figure(figsize=(7, 7))
    plt.pie(budgets, labels=movie_names, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    plt.title('Budget Distribution')
    chart2 = encode_plot()

    return render(request, 'app/budget_comparison.html', {
        'chart1': chart1,
        'chart2': chart2,
        'movies': movies
    })
def redi(request, id):  # Rename 'id' to 'movie_id'
    movie = get_object_or_404(Movie, id= id)  # Fetch the movie safely
    return render(request, "app/redi.html", {"movie": movie})

def my_view(request):
    messages.success(request, "Login successful!")  # Green success alert
    messages.error(request, "Invalid credentials!")  # Red error alert
    messages.warning(request, "Warning! Check your input.")  # Yellow warning
    return redirect("some_page")  # Redirect after setting messages

def verify_email(request):
    # Your email verification logic here
    return HttpResponse("Email Verified!")

def movie_list(request):
    movies = Movie.objects.all()  # Fetch all movies from the database
    return render(request, "movies.html", {"movies": movies})  # Pass movies to template

def profile(request):
    return render(request, 'registration/profile.html')