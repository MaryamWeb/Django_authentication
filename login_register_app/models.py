import re
from django.db import models
from datetime import date, datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validateRegister(self, post_data): 
        errors={}
        
        if len(post_data['first_name']) == 0 and len(post_data['password']) == 0 and len(post_data['email']) == 0:
            errors['all']='All fields are required'            
#--------------------------------------------First Name------------------------------------------
        else:
            if post_data['first_name'] == '' :
                errors['first_name']='First Name field is required'
            elif len(post_data['first_name']) < 2:
                errors['first_name']='First Name should be at least 2 characters'
            elif not post_data['first_name'].isalpha():
                errors['first_name']='First Name should only contain letters'
#--------------------------------------------Email-----------------------------------------------
            if post_data['email'] == '' :
                errors['email']='Email field is required'
            elif not EMAIL_REGEX.match(post_data['email']):
                errors['email'] = "Invalid email address!"
            if self.validate_email_exist(post_data) is True:
                errors['email']='Sorry. An account with that email already exists'
#-------------------------------------------Password-----------------------------------------
            if len(post_data['password']) < 8 :
                errors['password']='Password should be at least 8 characters'
            elif post_data['password'] != post_data['password_confirm']:
                errors['password'] = "Please make sure that both passwords match"
        return errors

    def validateLogin(self, post_data):
        error_pw={}
        if len(post_data['email']) == 0  or len(post_data['password']) == 0:
            error_pw['all']='Please type your email and password' 
        else:
            user = User.objects.filter(email=post_data['email'].lower()) 
            print(user)
            if len(user) < 1:
                error_pw['email']='Sorry. This email does not exist in our database'
                return  error_pw
            current_logged_user = user[0]  #we know that we only have 1 user with that email since we preveted duplicated emails
            check_password = bcrypt.checkpw(post_data['password'].encode(), current_logged_user.password.encode()) 
            if not check_password:
                error_pw['password']='Your email/password combination is incorrect'
        return error_pw

    def validate_email_exist(self, post_data):
            check_email_exist=len(self.filter(email=post_data['email'].lower()))
            if check_email_exist > 0:
                return True
            return False

class User(models.Model):
    first_name= models.CharField(max_length=40)
    email= models.EmailField()
    password= models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return f'<User object: ID:{self.id} First Name:{self.first_name} Email:{self.email}>'