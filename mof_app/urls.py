from django.urls import path
from . import views
from .views import verify_email, profile, budget_comparison, movie_detail
from django.urls import path,include


urlpatterns = [
 
  
   path('',views.reg),
   path('login/', views.login, name='login'),
   path('register/',views.reg, name='usr_reg'),
   path('verify/<int:user_id>/', verify_email, name='verify_email'), 
   path('dashboard/', views.dashboard, name='dashboard'),
   path('add_movies/', views.add_movie, name='add_movie'),
   path('delete_movie/<int:movie_id>/', views.delete_movie, name='delete_movie'), 
   path('movie/<int:id>/', views.movie_detail, name='movie_detail'),
   path("register/",views.reg, name="reg"), 
   path("login/", views.login, name="login"), 
   path('profile/', profile, name='profile'),
   path("logout/", views.logout_view, name="logout_view"), 
   path('add_movie/', views.add_movie, name='add_movie'),
   path('budget_comparison/', budget_comparison, name='budget_comparison'),
  
   path('movie/<int:id>/', views.movie_detail, name='movie_detail'),
   path('redi/<int:id>/', views.redi, name='redi'),
   path('profile/', views.profile, name='profile'),
   path('movies/', views.movie_list, name='movie_list'), 

   path('', views.movie_list, name='movie_list'),
   path('movie/<int:id>/', movie_detail, name='movie_detail'),
   path('movie/<int:movie_id>/add_expense/', views.add_expense, name='add_expense'),


    
  


]