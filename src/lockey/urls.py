"""lockey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

urlpatterns = [
    path('api/v1/users/', include('apps.user.api.urls', namespace='users')),
    path('api/v1/teams/', include('apps.team.api.urls', namespace='teams')),
    path('api/v1/credentials/', include('apps.credential.api.urls', namespace='credentials')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
]
