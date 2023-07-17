from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('browse/', views.browse_phones, name='browse_phones'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('phone/<int:phone_id>/', views.phone_detail, name='phone_detail'),
    path('recommendations/', views.recommended_phones, name='recommended_phones'),
    path('rate_phone/', views.rate_phone, name='rate_phone'),
]