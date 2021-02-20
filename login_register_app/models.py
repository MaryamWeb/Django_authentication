from django.db import models
from datetime import date, datetime

class User(models.Model):
    first_name= models.CharField(max_length=40)
    email= models.EmailField()
    password= models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<User object: ID:{self.id} First Name:{self.first_name} Email:{self.email}>'