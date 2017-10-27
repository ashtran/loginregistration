from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def validate_login(self,post_data):
        errors={}
        if len(self.filter(email=post_data['email']))>0:
            user=self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['login']="Email/password is incorrect"
        else:
            errors['login']="Email/password is incorrect"
        return errors

    def valid_login(self,post_data):
        if len(self.filter(email=post_data['email']))>0:
            user=self.filter(email=post_data['email'])[0]
        return user

    def validate_registration(self,post_data):
        errors={}
        for field,value in post_data.iteritems():
            if len(value)<1:
                errors[field]="{} field is required".format(field.replace('_',''))
            if field == "first_name" or field =="last_name":
                if not field in errors and len(value) < 3:
                    errors[field]="{} field must be at least 3 characters".format(field.replace('_',''))
            if field == "password":
                if not field in errors and len(value) <8:
                    errors[field]="{} field must be at least 8 characters".format(field.replace('_',''))
        if not "email" in errors and not re.match(EMAIL_REGEX, post_data['email']):
            errors['email']="Invalid Email"
        else:
            if len(self.filter(email=post_data['email']))> 1:
                errors['email']= "Email is already in use"
        if post_data['password'] != post_data['confirmpw']:
            errors['password']="Passwords do not match"
        return errors

    def valid_user(self,post_data):
        hashed= bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt(5))
        new_user= self.create(
            first_name= post_data['first_name'],
            last_name= post_data['last_name'],
            email= post_data['email'],
            password= hashed
        )
        return new_user

class User(models.Model):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "id:{} first_name:{} last_name:{} email:{} created_at:{} updated_at:{}".format(self.id,self.first_name,self.last_name,self.email,self.created_at,self.updated_at)


# Create your models here.
