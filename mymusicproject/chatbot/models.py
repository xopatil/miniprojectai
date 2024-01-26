# mymusicproject/chatbot/models.py
from django.db import models

class UserInteraction(models.Model):
    user = models.CharField(max_length=255)
    message = models.TextField()

class Recommendation(models.Model):
    user = models.CharField(max_length=255)
    message = models.TextField()
    sentiment = models.CharField(max_length=50)



    