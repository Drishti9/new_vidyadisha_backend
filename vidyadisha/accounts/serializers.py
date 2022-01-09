from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}
        
        def create(self, validated_data):
            user = User.objects.create_user(
                email=validated_data["email"],
                password=validated_data["password"],
                last_name=validated_data["last_name"],
                first_name=validated_data["first_name"]
                )
            return user

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ( "id","email","first_name",
                   "last_name", "standard","institute",
                   "requiresDonation","requiresMentor","requiresTutor","password")
                   
        extra_kwargs = {"password" : {"write_only":True}}
        
        def create(self,validated_data):
            user = Student.objects.create_user( 
                email=validated_data["email"],
                standard=validated_data["standard"],
                password=validated_data["password"],
                institute=validated_data["institute"],
                is_student=True,
                is_mentor=False,
                is_tutor=False,
                is_donor=False,
                requiresDonation = validated_data["requiresDonation"],
                requiresMentor = validated_data["requiresMentor"],
                requiresTutor = validated_data["requiresTutor"],
                last_name=validated_data["last_name"],
                first_name=validated_data["first_name"],
                )
            return user

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ( "id","email","first_name",
                   "last_name", "experience_in_years","password")
                   
        extra_kwargs = {"password" : {"write_only":True}}
        
        def create(self,validated_data):
            user = Student.objects.create_user( 
                email=validated_data["email"],
                standard=validated_data["standard"],
                password=validated_data["password"],
                experience_in_years=validated_data["experience_in_years"],
                is_student=False,
                is_mentor=False,
                is_tutor=True,
                is_donor=False,
                last_name=validated_data["last_name"],
                first_name=validated_data["first_name"],
                )
            return user

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ( "id","email","first_name",
                   "last_name", "occupation","password")
                   
        extra_kwargs = {"password" : {"write_only":True}}
        
        def create(self,validated_data):
            user = Student.objects.create_user( 
                email=validated_data["email"],
                standard=validated_data["standard"],
                password=validated_data["password"],
                occupation=validated_data["occupation"],
                is_student=False,
                is_mentor=True,
                is_tutor=False,
                is_donor=False,
                last_name=validated_data["last_name"],
                first_name=validated_data["first_name"],
                )
            return user

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ( "id","email","first_name",
                   "last_name", "donation_type","password")
                   
        extra_kwargs = {"password" : {"write_only":True}}
        
        def create(self,validated_data):
            user = Student.objects.create_user( 
                email=validated_data["email"],
                standard=validated_data["standard"],
                password=validated_data["password"],
                donation_type=validated_data["donation_type"],
                is_student=False,
                is_mentor=False,
                is_tutor=False,
                is_donor=True,
                last_name=validated_data["last_name"],
                first_name=validated_data["first_name"],
                )
            return user