# chatbot/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    # Add more URL patterns as needed
]
