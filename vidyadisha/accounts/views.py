
from django.shortcuts import render
from django.http import HttpResponse
from .serializers import * 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

class RegisterUser(generics.GenericAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user.is_student:
            role = "STUDENT"
        elif user.is_tutor:
            role = "TUTOR"
        elif user.is_mentor:
            role = "MENTOR"
        elif user.is_donor:
            role = "DONOR"
        else:
            role = "DEFAULT"
        return Response({"role": role}, status=HTTP_200_OK)

class RegisterStudent(generics.GenericAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get(self, request):
        users = Student.objects.all()
        serializer = StudentSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user.is_student:
            role = "STUDENT"
        elif user.is_tutor:
            role = "TUTOR"
        elif user.is_mentor:
            role = "MENTOR"
        elif user.is_donor:
            role = "DONOR"
        else:
            role = "DEFAULT"
        return Response({"role": role}, status=HTTP_200_OK)

class RegisterMentor(generics.GenericAPIView):
    serializer_class = MentorSerializer
    queryset = Mentor.objects.all()

    def get(self, request):
        users = Mentor.objects.all()
        serializer = MentorSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user.is_student:
            role = "STUDENT"
        elif user.is_tutor:
            role = "TUTOR"
        elif user.is_mentor:
            role = "MENTOR"
        elif user.is_donor:
            role = "DONOR"
        else:
            role = "DEFAULT"
        return Response({"role": role}, status=HTTP_200_OK)

class RegisterDonor(generics.GenericAPIView):
    serializer_class = DonorSerializer
    queryset = Donor.objects.all()

    def get(self, request):
        users = Donor.objects.all()
        serializer = DonorSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user.is_student:
            role = "STUDENT"
        elif user.is_tutor:
            role = "TUTOR"
        elif user.is_mentor:
            role = "MENTOR"
        elif user.is_donor:
            role = "DONOR"
        else:
            role = "DEFAULT"
        return Response({"role": role}, status=HTTP_200_OK)


class RegisterTutor(generics.GenericAPIView):
    serializer_class = TutorSerializer
    queryset = Tutor.objects.all()

    def get(self, request):
        users = Tutor.objects.all()
        serializer = TutorSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):   

        #sub_names=request.data.pop("subject")
        #print(sub_names)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        #sub_names, sub_type=serializer.save()

        """for each in sub_names:
            s=accounts.models.Subject.objects.filter(name=each.lower()).first()
            if not s:
                s=accounts.models.Subject.objects.create(name=each)
            user.subject.add(s)"""

        if user.is_student:
            role = "STUDENT"
        elif user.is_tutor:
            role = "TUTOR"
        elif user.is_mentor:
            role = "MENTOR"
        elif user.is_donor:
            role = "DONOR"
        else:
            role = "DEFAULT"
        return Response({"role": role}, status=HTTP_200_OK)
        #return Response({"subnames": sub_names, "sub_type":sub_type}, status=HTTP_200_OK)


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

class StuRequiringMentorViewSet(viewsets.ModelViewSet):
    queryset=Student.objects.filter(requiresMentor=True)
    serializer_class=StudentSerializer

class StuRequiringDonorViewSet(viewsets.ModelViewSet):
    queryset=Student.objects.filter(requiresDonation=True)
    serializer_class=StudentSerializer

class StuRequiringTutorViewSet(viewsets.ModelViewSet):
    queryset=Student.objects.filter(requiresTutor=True)
    serializer_class=StudentSerializer

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