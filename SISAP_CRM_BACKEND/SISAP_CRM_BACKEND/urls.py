"""
URL configuration for SISAP_CRM_BACKEND project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

# Define the URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URL
    path('api/', include('crm.urls')),  # Include the URLs from the crm app
]
