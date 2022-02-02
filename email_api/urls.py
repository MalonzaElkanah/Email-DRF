"""email_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from drf_autodocs.views import TreeView

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('settings/', views.EmailSettingListCreateAPIView.as_view(), name='email-settings'),
    path('settings/<int:pk>/', views.EmailSettingUpdateAPIView.as_view(), name='email-settings'),
    path('inbox/<int:pk>/', views.inbox_apiview, name='email-inbox'),
    path('', TreeView.as_view(), name='api-tree'),
]
