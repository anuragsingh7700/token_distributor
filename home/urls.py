from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name="home"),
    path('login/', auth_views.LoginView.as_view(template_name ='login.html'),name='login'),
    path('signup/',views.signup,name="signup"),
    path('logout/', views.logout_view, name='logout'),
    path('events/',views.event_list,name='event_list'),
    path('token/<id>',views.gen_token,name="gen_token"),
    path('view/',views.token_list,name="token_list")
]