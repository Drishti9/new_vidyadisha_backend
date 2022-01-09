
from django.shortcuts import render
from django.http import HttpResponse
from .serializers import * 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer

class TutorViewSet(viewsets.ModelViewSet):
    queryset=Tutor.objects.all()
    serializer_class=TutorSerializer

class MentorViewSet(viewsets.ModelViewSet):
    queryset=Mentor.objects.all()
    serializer_class=MentorSerializer

class DonorViewSet(viewsets.ModelViewSet):
    queryset=Donor.objects.all()
    serializer_class=DonorSerializer

""""
@api_view(['GET'])
def UserList(request):
    customuser = User.objects.all()
    serializer = UserSerializer(customuser,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def StudentList(request):
    student = Student.objects.all()
    serializer = UserSerializer(student,many=True)
    return Response(serializer.data)

"""