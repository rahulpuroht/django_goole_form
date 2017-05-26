from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from datetime import datetime
import time
import uuid
import requests
import json
import datetime


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        Token.objects.create(user=user)
        return user

    def create_superuser(self, email, password): 
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    User Table for Avaana 
    """
    email = models.EmailField(('Email Address'), max_length=255, unique=True)
    first_name = models.CharField(('First Name'), max_length=50, blank=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(('created_at'), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(('updated_at'), auto_now=True, auto_now_add=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):
        return self.email

    class Meta:
        """
        Meta Class to show Desired name of Table in Admin.py
        """
        verbose_name = 'Form User'
        verbose_name_plural = 'Forms User'


class AnswerType(models.Model):
    """docstring for AnswerType"""
    answere_type = models.CharField(('Answere Type'), max_length=50, blank=False)


class Forms(models.Model):
    """docstring for AnswerType"""
    form_owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    form_name = models.CharField(('Form Name'), max_length=50, blank=False)
    form_description = models.TextField(('Form Description'), max_length=500, blank=True)

class question_answer(models.Model):
    form_owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    form_id = models.ForeignKey(Forms, on_delete=models.CASCADE)
    question = models.CharField(('Question'), max_length=500, blank=False)
    answer_type = models.IntegerField(('Answer Type'), blank=False)

class form_response_id(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)
        

class form_response(models.Model):
    response_id = models.ForeignKey(form_response_id, on_delete=models.CASCADE)
    question_id = models.ForeignKey(question_answer, on_delete=models.CASCADE)
    answere = models.CharField(('Answere'), max_length=100, blank=True,null=True)

        