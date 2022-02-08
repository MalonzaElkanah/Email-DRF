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
    path('emails/', views.EmailSettingListCreateAPIView.as_view(), name='emails'),
    path('emails/<int:pk>/', views.EmailSettingUpdateAPIView.as_view(), name='email'),
    path('emails/<int:pk>/test/', views.test_settings, name='email-test'),
    path('emails/<int:pk>/inbox/', views.inbox_apiview, name='email-inbox'),
    path('emails/<int:pk>/compose/', views.ComposeEmailAPIView.as_view(), name = 'email-compose'),
    path('emails/<int:pk>/label/<slug:label>/', views.label_mails, name = 'email-labels'),    
    path('emails/<int:pk>/label/<slug:label>/<int:email_id>/', views.read_email, name = 'email-view'),
    path('emails/<int:pk>/label/<slug:label>/<int:email_id>/attachment/<int:attachment_id>/', 
        views.get_attachment, name = 'attachment-file'),

    path('', TreeView.as_view(), name='api-tree'),
]
