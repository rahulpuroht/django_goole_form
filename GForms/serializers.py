import itertools
from datetime import datetime, timedelta
from pytz import timezone
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from GForms.models import *
from django.db.models import Avg, Sum
from django.contrib.auth import get_user_model
from django.utils.timesince import timesince
import requests


##### SERIALIZER OF USER SERIALIZER #######
class UserSerializer(serializers.ModelSerializer):
    """docstring for UserSerializer"""
    password = serializers.CharField(write_only=True, min_length=8, error_messages={"blank": "Password cannot be empty.", "min_length": "Password too short."})
    class Meta:
        """Doc string for class Meta"""
        model = get_user_model()
        fields = '__all__'

    def create(self, validated_data):
        user = MyUser(email=validated_data['email'],
                      first_name=validated_data['first_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class AddQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        """Doc string for class Meta"""
        model = question_answer
        fields = '__all__'

class AddFormSerializer(serializers.ModelSerializer):

    form_details = SerializerMethodField()
    def get_form_details(self, obj):
       return AddQuestionSerializer(question_answer.objects.filter(form_id=obj.id),many=True).data

    form_response = SerializerMethodField()
    def get_form_response(self, obj):
       return FormResponseIDSerializer(form_response_id.objects.filter(form_id=obj.id),many=True).data

    class Meta:
        """Doc string for class Meta"""
        model = Forms
        fields = '__all__'


class AnswerTypeSerializer(serializers.ModelSerializer):

    class Meta:
        """Doc string for class Meta"""
        model = AnswerType
        fields = '__all__'


class AddQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        """Doc string for class Meta"""
        model = question_answer
        fields = '__all__'

class FormResponseIDSerializer(serializers.ModelSerializer):

    question_response = SerializerMethodField()
    def get_question_response(self, obj):
       return FormResponseSerializer(form_response.objects.filter(response_id=obj.id),many=True).data
    class Meta:
        """Doc string for class Meta"""
        model = form_response_id
        fields = '__all__'

class FormResponseSerializer(serializers.ModelSerializer):


    question = SerializerMethodField()
    def get_question(self, obj):
       return obj.question_id.question

    answer_type = SerializerMethodField()
    def get_answer_type(self, obj):
       return obj.question_id.answer_type
    class Meta:
        """Doc string for class Meta"""
        model = form_response
        fields = '__all__'