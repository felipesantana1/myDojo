from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

PASSWORD_REGEX = re.compile(r'[A-Z0-9]')

class UsersManager(models.Manager):

    def regValidator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = 'Name field must contain at least 3 characters'
        if len(postData['username']) < 3:
            errors['username'] = 'Username field must contain at least 3 characters'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must contain more than 8 characters'
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = 'Invalid email/password'
        if postData['password'] != postData['confirmPW']:
            errors['password'] = 'Passwords do not match!'
        return errors

    def logValidator(self, postData):
        errors = {}
        if postData['username'] < 1:
            errors['username'] = 'No username/password detected. Please try again.'
        if postData['password'] < 1:
            errors['password'] = 'No username/password detected. Please try again.'
        if not Users.objects.filter(username=postData['username']):
            errors['login'] = 'Invalid username/password. Please try again or register'
        elif not bcrypt.checkpw(postData['password'].encode(), Users.objects.get(username=postData['username']).password.encode()):
            errors['login'] = 'Invalid username/password. Please try again or register'
        return errors

class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class Trips(models.Model):
    plan = models.CharField(max_length=255)
    start =  models.CharField(max_length=255)
    end =  models.CharField(max_length=255)
    user = models.ForeignKey(Users, related_name='planned_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Destinations(models.Model):
    name = models.CharField(max_length=255)
    trip = models.ForeignKey(Trips, related_name='trip_to')
    user = models.ForeignKey(Users, related_name='planned_to')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)