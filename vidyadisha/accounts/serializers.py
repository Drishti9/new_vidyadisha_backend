from .models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name","password", "is_student", "is_tutor", "is_donor", "is_mentor")
        extra_kwargs = {"password": {"write_only": True, "required":False}}
        
    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #         email=validated_data["email"],
    #         password=validated_data["password"],
    #         last_name=validated_data["last_name"],
    #         first_name=validated_data["first_name"]
    #         )
    #     return user

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ( "id","email","first_name",
                   "last_name", "standard","institute",
                   "requiresDonation","requiresMentor","requiresTutor","password", "mobile", "address")
                   
        extra_kwargs = {"password" : {"write_only":True, 'required':False}, "standard":{"required":False}, "institute":{"required":False}, "email":{"required":False}}
        
    def create(self,validated_data):
        user = Student.objects.create_user( 
            email=validated_data["email"],
            standard=validated_data["standard"],
            password=validated_data["password"],
            institute=validated_data["institute"],
            requiresDonation = validated_data["requiresDonation"],
            requiresMentor = validated_data["requiresMentor"],
            requiresTutor = validated_data["requiresTutor"],
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
            mobile=validated_data["mobile"],
            address=validated_data["address"]
            )
        return user

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ( "id","name")
        
        def create(self,sub_name):
            sub = Subject.objects.create( 
                name=sub_name
                )
            return sub

class TutorSerializer(WritableNestedModelSerializer):
    subject=SubjectSerializer(many=True, required=False)
    experience_in_years=serializers.IntegerField(required=False)

    class Meta:
        model = Tutor
        fields = ( "id","email","first_name",
                   "last_name", "subject","experience_in_years","password","mobile", "address")
                   
        extra_kwargs = {"password" : {"write_only":True, 'required':False}, "email":{'required':False}, "experience_in_years":{'required':False}, "subject":{'required':False}}
        
    def create(self,validated_data):
        sub_names=validated_data.pop("subject")

        user = Tutor.objects.create_user( 
            email=validated_data["email"],
            password=validated_data["password"],
            experience_in_years=validated_data["experience_in_years"],
            #is_student=False,
            #is_mentor=False,
            # is_tutor=True,
            # is_donor=False,
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
            mobile=validated_data["mobile"],
            address=validated_data["address"]
            )

        for each in sub_names:
            for key, value in each.items():
                s=accounts.models.Subject.objects.filter(name=value).first()
                if s is None:
                    s=accounts.models.Subject.objects.create(name=value)
                user.subject.add(s)     
        
        return user

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ( "id","email","first_name",
                   "last_name", "occupation","password", "mobile", "address")
                   
        extra_kwargs = {"password" : {"write_only":True, 'required':False}, "occupation":{'required':False}}
        
    def create(self,validated_data):
        user = Mentor.objects.create_user( 
            email=validated_data["email"],
            password=validated_data["password"],
            occupation=validated_data["occupation"],
            # is_student=False,
            # is_mentor=True,
            # is_tutor=False,
            # is_donor=False,
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
            mobile=validated_data["mobile"],
            address=validated_data["address"]
            )
        return user

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ( "id","email","first_name",
                   "last_name", "donation_type","password","mobile", "address")
                   
        extra_kwargs = {"password" : {"write_only":True, 'required':False}, "donation_type":{'required':False}}
        
    def create(self,validated_data):

        user = Donor.objects.create_user( 
            email=validated_data["email"],
            password=validated_data["password"],
            donation_type=validated_data["donation_type"],
            # is_student=False,
            # is_mentor=False,
            # is_tutor=False,
            # is_donor=True,
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
            mobile=validated_data["mobile"],
            address=validated_data["address"]
        )

        return user
