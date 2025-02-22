from django.urls import path
from . import views
from .views import verify_email
from django.urls import path,include


urlpatterns = [
 
  
   path('',views.reg),
   path('login/', views.login, name='login'),
   path('register/',views.reg, name='usr_reg'),
   path('verify/<int:user_id>/', verify_email, name='verify_email'), 
   path('dashboard/', views.dashboard, name='dashboard'),
   path('add_movies/', views.add_movie, name='add_movie'),
   
   

    
  


]