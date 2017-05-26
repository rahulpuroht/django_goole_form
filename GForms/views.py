# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from GForms.models import *
from django.conf import settings
from django.views.decorators.http import require_http_methods 
from django.shortcuts import render
from django.contrib import messages
from django.contrib import auth
from rest_framework.response import Response
from django.contrib.auth import (authenticate, get_user_model, login, logout,)
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import Permission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
from GForms.serializers import *
# from GForms.signals import *           
# Create your views here.
def landingpage(request):
    return render(request, 'index.html')

@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    params = request.data
    serializer = UserSerializer(data=params)
    if serializer.is_valid():
        result = serializer.save()
        payload = jwt_payload_handler(result)
        token = jwt.encode(payload, settings.SECRET_KEY)
        auth_token = token.decode('unicode_escape')
        return Response({"status":200, "Message":"Signup Successfull.", "User_Detail":serializer.data, "auth_token":auth_token}, headers={"Authorization":"JWT "+auth_token})
    else:
        return Response({"status":500, "Message":serializer.errors, "Error":serializer.errors[list(serializer.errors)[0]][0]})

###--- Login Api ---###
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request, format='json'):
    params = request.data
    print(params)
    try:

        user = get_user_model().objects.get(email=params['email'], is_active=True)
        user  = authenticate(username=user.email, password=params['password'])
        if user:
            # login(request, user)
            serializer = UserSerializer(user)
            user_profile = serializer.data
            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, settings.SECRET_KEY)
            auth_token = token.decode('unicode_escape')
            return Response({"status":200, "Message":"Login Successfully", "user":user_profile, "auth_token":auth_token})
        else:
            return Response({"status":500, "Message":"Invalid email and password combination."})
    except get_user_model().DoesNotExist:
        return Response({"status":500, "Message":"Invalid email and password combination."})

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def addform(request, format='json'):
    params = request.data
    user = request.user
    params['form_owner'] = user.id
    serailizer = AddFormSerializer(data=params)
    if serailizer.is_valid():
        serailizer.save()
        return Response({"status":200,"Message":"Form saved Successfully","id":serailizer.data['id']})
    else:
        print("Error in Add Form Serializer",serailizer.errors)
        return Response({"status":500,"Message":"Form not saved Successfully",'error':serailizer.errors})



@api_view(['GET'])
@permission_classes((AllowAny,))
def answerType(request, format='json'):
    params = request.data
    answer_type = AnswerType.objects.all()
    serailizer = AnswerTypeSerializer(answer_type,many=True)
    return Response({"status":200,"Message":"Form saved Successfully","type":serailizer.data})



@api_view(['GET'])
@permission_classes((AllowAny,))
def allforms(request, format='json'):
    params = request.data
    all_forms = Forms.objects.all()
    formserailizer = AddFormSerializer(all_forms,many=True)
    return Response({"status":200,"Message":"Form saved Successfully","all_forms":formserailizer.data})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def yourforms(request, format='json'):
    params = request.data
    user = request.user
    your_forms = Forms.objects.filter(form_owner=user.id)
    formserailizer = AddFormSerializer(your_forms,many=True)
    return Response({"status":200,"Message":"Form saved Successfully","your_forms":formserailizer.data})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def addquestion(request, format='json'):
    params = request.data
    user = request.user
    params['form_owner'] = user.id
    serailizer = AddQuestionSerializer(data=params)
    if serailizer.is_valid():
        serailizer.save()
        all_question = question_answer.objects.filter(form_owner=user.id,form_id=params['form_id'])
        Questionserailizer = AddQuestionSerializer(all_question,many=True)
        return Response({"status":200,"Message":"Question saved Successfully","question":Questionserailizer.data})
    else:
        print("Error in Add Question Serializer",serailizer.errors)
        return Response({"status":500,"Message":"Question not saved Successfully",'error':serailizer.errors})


@api_view(['POST'])
@permission_classes((AllowAny,))
def saveResponse(request, format='json'):
    params = request.data
    print(params)

    serailizer = FormResponseIDSerializer(data={"form":params[0]['form_id']})
    if serailizer.is_valid():
        serailizer.save()
        for answere in params:
            answere['response_id'] = serailizer.data['id']
        serializer = FormResponseSerializer(data=params,many=True)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        return Response({"status":200,"Message":"Response saved Successfully"})
    else:
        print("Error in saveResponse Serializer",serailizer.errors)
        return Response({"status":500,"Message":"Response not saved Successfully",'error':serailizer.errors})
