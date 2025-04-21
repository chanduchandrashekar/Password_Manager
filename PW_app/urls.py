
from django.urls import path,include
from . import views

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('register/',views.register,name='register'),
    path('home/',views.home_view,name="home"),
    path('dashbord/',views.dashbord,name='dashbord'),
    path('add_password/',views.add_password,name='add_password'),
    path('save_password/', views.save_password, name='save_password'),
    path('logout/',views.logout_view,name='logout'),
    path('delete/<int:password_id>/',views.delete_savedpassword,name="delete_savedpassword"),
    path('edit_existing_password/<int:password_id>/',views.edit_existing_password,name='edit_existing_password'),
    
]
