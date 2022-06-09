import email
from django.shortcuts import render
from django.http import HttpResponse
from sympy import sring
from .serializers import * 
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json

from twilio.rest import Client
from sms import send_sms

from rest_framework_simplejwt.tokens import RefreshToken

from django.core.mail import send_mail

def send_message(request):
    data = json.loads(request.body)
    phone=data.get('phone')
    description=data.get('description')


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    if user.is_student:
        user_type="Student"
    elif user.is_tutor:
        user_type="Tutor"
    elif user.is_mentor:
        user_type="Mentor"
    elif user.is_donor:
        user_type="Donor"
    else:
        user_type="None"

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': user.id,
        'type':user_type,
        'first_name':user.first_name
    }

@api_view(['POST',])
@permission_classes((AllowAny,))
def login_view(request):

    #POST API for login
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    if email is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter email"
            }
        }, status=400)
    elif password is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter password"
            }
        }, status=400)

    # authentication user
    user = authenticate(email=email, password=password)
    if user is not None:
        #login(request, user)
        #return JsonResponse({"success": "User has been logged in"})
        user_id = User.objects.get(email=email)
        data = get_tokens_for_user(user_id)
        return Response(data, status=HTTP_200_OK)
        #return JsonResponse({user})
    return JsonResponse(
        {"errors": "Invalid credentials"},
        status=400,
    )

"""@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def logout_view(request):
    logout(request)
    data = {'success': 'Sucessfully logged out'}
    return Response(data=data, status=HTTP_200_OK)"""

# Create your views here.


class UserInformation(generics.GenericAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        for each in serializer.data:
            data=each
            if serializer.data['is_student']:
                type='student'
            elif serializer.data['is_mentor']:
                type='mentor'
            elif serializer.data['is_tutor']:
                type='tutor'
            elif serializer.data['is_donor']:
                type='donor'
            #data['type']=type
            print(data)
        
        print(serializer.data)
        return Response(serializer.data)


class UserInformationWithId(generics.GenericAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)
        #print(serializer.data['is_student'])
        type=''
        if serializer.data['is_student']:
            type='student'
        elif serializer.data['is_mentor']:
            type='mentor'
        elif serializer.data['is_tutor']:
            type='tutor'
        elif serializer.data['is_donor']:
            type='donor'
        data=serializer.data
        data['type']=type
        print(data)
        return Response(data)

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    #permission_classes=[IsAuthenticated]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset=Subject.objects.all()
    serializer_class=SubjectSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer
    #permission_classes=[IsAuthenticated]

class TutorViewSet(viewsets.ModelViewSet):
    queryset=Tutor.objects.all()
    serializer_class=TutorSerializer

class MentorViewSet(viewsets.ModelViewSet):
    queryset=Mentor.objects.all()
    serializer_class=MentorSerializer

class DonorViewSet(viewsets.ModelViewSet):
    queryset=Donor.objects.all()
    serializer_class=DonorSerializer
 
###need based views
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
    customuser = CustomUser.objects.all()
    serializer = UserSerializer(customuser,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def StudentList(request):
    student = Student.objects.all()
    serializer = UserSerializer(student,many=True)
    return Response(serializer.data)
"""

class RegisterUser(generics.GenericAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        print(request.data)
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

@api_view(['POST',])
def sendemail(request):
    data = json.loads(request.body)
    #message_subject= data.get('subject')
    name=data.get('name')
    message_body= data.get('body')
    message_remail= data.get('receiver')
    contact=data.get('contact')
    student_name=data.get('student_name')
        
    print("request geenrated")
    print(message_remail, type(message_remail))
    #f"Welcome to VidyaDisha {name}, {student_name} wants your help.\nVidyaDisha is an online community aimed at connecting the less privileged students to adequately-educated classes of the society for guidance, tuition and sponsorship. We received a request to invite you to our website,www.vidyadisha.com and join our community in a role best suitable and convenient to you(Mentor/ Tutor/ Donor). Hope to see you soon as our valued member. In case of any queries, please mail us at vidyadisha.office@gmail.com.\n\n{message_body}",
    
    send_mail(
        'Invitation to Vidyadisha',
        message=f"Welcome to VidyaDisha {name}, {student_name} wants your help.\nVidyaDisha is an online community aimed at connecting the less privileged students to adequately-educated classes of the society for guidance, tuition and sponsorship. We received a request to invite you to our website,www.vidyadisha.com and join our community in a role best suitable and convenient to you(Mentor/ Tutor/ Donor). Hope to see you soon as our valued member. In case of any queries, please mail us at vidyadisha.office@gmail.com.\n\n{message_body}",
        #'heellllo',
        from_email='vidyadisha.office@gmail.com',
        recipient_list=[message_remail],
        fail_silently=False,
    )

    """send_sms(
    'Here is the message',
    '+12065550100',
    ['+919769004201', '+919324185450']
    )"""

    # account_sid = 'ACbbc81ce39f850176d36eb33077b64e2c'
    # auth_token = '3ac9f36545703c5ee4c5fb8291a89858' 
    # client = Client(account_sid, auth_token) 
    # message = client.messages.create( 
    #                 body = f"Welcome to VidyaDisha {name}, {student_name} wants your help.\nVidyaDisha is an online community aimed at connecting the less privileged students to adequately-educated classes of the society for guidance, tuition and sponsorship. We received a request to invite you to our website,www.vidyadisha.com and join our community in a role best suitable and convenient to you(Mentor/ Tutor/ Donor). Hope to see you soon as our valued member. In case of any queries, please mail us at vidyadisha.office@gmail.com.\n\n{message_body}",
    #                 from_ = '+17755425836',
    #                 to = f'+91{contact}' 
    #                 )
    # print(message.sid)

    return Response(status=HTTP_200_OK)