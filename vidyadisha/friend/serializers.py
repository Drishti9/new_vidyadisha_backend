from dataclasses import field
from unittest import result

from django.shortcuts import redirect
from .models import *
#from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import User

###Only allow get
class FriendListSerializer(serializers.ModelSerializer):
    myself=serializers.PrimaryKeyRelatedField(many=False, queryset=get_user_model().objects.all())
    people=serializers.PrimaryKeyRelatedField(many=True,  queryset=get_user_model().objects.all())

    class Meta:
        model=FriendList
        fields=['myself', 'people']

    """def create(self, validated_data):
        myself_key=validated_data.pop("myself")
        people_keys=validated_data.pop("people")
        print(myself_key)
        print(people_keys)

        friend_list=FriendList.objects.filter(myself=myself_key).first()

        if friend_list==None:
            #myself_object=get_user_model().objects.get(email=myself_key)
            friend_list=FriendList.objects.create(myself=myself_key)

        for each in people_keys:
            friend_list.add_friend(each)

            #adding acceptor to sender's friendlist
            friend_list_of_friend=FriendList.objects.filter(myself=myself_key).first()
            if friend_list_of_friend==None:
                friend_list_of_friend=FriendList.objects.create(myself=myself_key)
            friend_list_of_friend.add_friend(myself_key)

        return friend_list"""

class UnFriendSerializer(serializers.ModelSerializer):
    remover=serializers.PrimaryKeyRelatedField(many=False, queryset=get_user_model().objects.all())
    removee=serializers.PrimaryKeyRelatedField(many=False,  queryset=get_user_model().objects.all())

    class Meta:
        model=FriendList
        fields=['remover', 'removee']

    def create(self, validated_data):
        myself_object=validated_data.pop("remover")
        person_object=validated_data.pop("removee")

        friend_list=FriendList.objects.filter(myself=myself_object).first()

        if friend_list==None:
            return None
        
        friend_list.unfriend(person_object)

        return friend_list

class FriendRequestSerializer(serializers.ModelSerializer):
    sender=serializers.PrimaryKeyRelatedField(many=False, queryset=get_user_model().objects.all())
    receiver=serializers.PrimaryKeyRelatedField(many=False, queryset=get_user_model().objects.all())

    class Meta:
        model=FriendRequest
        fields=['sender', 'receiver', 'isActive']

    def create(self, validated_data):
        sender_object=validated_data.pop("sender")
        receiver_object=validated_data.pop("receiver")

        return FriendRequest.objects.create(sender=sender_object, receiver=receiver_object)

class FriendRequestAcceptSerializer(serializers.ModelSerializer):
    sender=serializers.PrimaryKeyRelatedField(many=False, queryset=get_user_model().objects.all())
    receiver=serializers.PrimaryKeyRelatedField(many=False, queryset=get_user_model().objects.all())

    class Meta:
        model=FriendRequest
        fields=['sender', 'receiver']

    def create(self, validated_data):
        sender_object=validated_data.pop("sender")
        receiver_object=validated_data.pop("receiver")

        friend_request=FriendRequest.objects.filter(sender=receiver_object).filter(receiver=sender_object).first()
        if friend_request:
            friend_request.accept()
            return friend_request

class FriendRequestDeclineSerializer(serializers.ModelSerializer):
    sender=serializers.PrimaryKeyRelatedField(many=False, queryset=get_user_model().objects.all())
    receiver=serializers.PrimaryKeyRelatedField(many=False, queryset=get_user_model().objects.all())

    class Meta:
        model=FriendRequest
        fields=['sender', 'receiver']

    def create(self, validated_data):
        sender_object=validated_data.pop("sender")
        receiver_object=validated_data.pop("receiver")

        friend_request=FriendRequest.objects.filter(sender=receiver_object).filter(receiver=sender_object).first()
        if friend_request:
            friend_request.decline(sender_object, receiver_object)
            return friend_request