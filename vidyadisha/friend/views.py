from django.shortcuts import render
from sympy import ground_roots, true
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework import generics
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

# Create your views here.
class FriendListViewSet(generics.GenericAPIView):
    http_method_names = ["get"]

    serializer_class = FriendListSerializer
    queryset = FriendList.objects.all()

    def get(self, request, pk):
        myself_object=get_user_model().objects.get(id=pk)
        friend_list_obj = FriendList.objects.filter(myself=myself_object).first()
        if not friend_list_obj:
            friend_list_obj=FriendList.objects.create(myself=myself_object)
        serializer = FriendListSerializer(friend_list_obj)
        return Response(serializer.data)

"""    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_200_OK)"""

class UnfriendView(generics.GenericAPIView):
    http_method_names = ["post"]

    serializer_class=UnFriendSerializer
    queryset=FriendList.objects.all()

    def post(self, request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_200_OK)

class FriendRequestPendingView(generics.GenericAPIView):
    http_method_names = ["get"]
    serializer_class=FriendRequestSerializer
    queryset=FriendList.objects.all()

    def get(self, request, pk):
        sender_object=get_user_model().objects.filter(id=pk).first()
        tuples = FriendRequest.objects.filter(sender=sender_object).filter(isActive=True)
        serializer = FriendRequestSerializer(tuples, many=True)
        return Response(serializer.data)

class FriendRequestAcceptancePendingView(generics.GenericAPIView):
    http_method_names = ["get"]
    serializer_class=FriendRequestSerializer
    queryset=FriendList.objects.all()

    def get(self, request, pk):
        receiver_object=get_user_model().objects.filter(id=pk).first()
        tuples = FriendRequest.objects.filter(receiver=receiver_object).filter(isActive=True)
        serializer = FriendRequestSerializer(tuples, many=True)
        return Response(serializer.data)


class FriendRequestView(generics.GenericAPIView):
    serializer_class=FriendRequestSerializer
    queryset=FriendList.objects.all()

    def get(self, request):
        tuples = FriendRequest.objects.all()
        serializer = FriendRequestSerializer(tuples, many=True)
        return Response(serializer.data)

    """def get(self, request):
        tuples = FriendRequest.objects.all()
        serializer = FriendRequestSerializer(tuples, many=True)
        return Response(serializer.data)"""

    def post(self, request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_200_OK)

class FriendRequestAcceptView(generics.GenericAPIView):
    http_method_names = ["post"]

    serializer_class=FriendRequestAcceptSerializer
    queryset=FriendRequest.objects.all()

    def post(self, request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_200_OK)

class FriendRequestDeclineView(generics.GenericAPIView):
    http_method_names = ["post"]

    serializer_class=FriendRequestDeclineSerializer
    queryset=FriendRequest.objects.all()

    def post(self, request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_200_OK)


#####Group related views

class GroupViewSet(generics.GenericAPIView):
    http_method_names = ["get"]

    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def get(self, request, pk):
        group_object=Group.objects.get(id=pk)
        serializer = GroupSerializer(group_object)
        return Response(serializer.data)

class GroupListViewSet(generics.GenericAPIView):
    http_method_names=["get"]

    serializer_class=GroupListSerializer
    queryset=GroupList.objects.all()

    def get(self, request, pk):
        person_object=get_user_model().objects.get(id=pk)
        group_list=GroupList.objects.filter(person=person_object).first()
        if not group_list:
            group_list=GroupList.objects.create(person=person_object)
        serializer = GroupListSerializer(group_list)
        return Response(serializer.data)

class PostGetViewSet(generics.GenericAPIView):
    http_method_names=["get", "post"]

    serializer_class=PostSerailizer
    queryset=Post.objects.all()

    def get(self, request, pk):
        group_object=Group.objects.get(id=pk)
        tuples=Post.objects.filter(group=group_object)
        serializer=PostSerailizer(tuples, many=True)
        return Response(serializer.data)

class PostInsertViewSet(generics.GenericAPIView):
    http_method_names=["post"]

    serializer_class=PostSerailizer
    queryset=Post.objects.all()

    def post(self, request):
        group_object=Group.objects.get(id=request.data['group'])
        owner_object=get_user_model().objects.get(id=request.data['owner'])


        if owner_object in group_object.members.all():
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=HTTP_200_OK)
        elif owner_object.is_student:
            if Student.objects.get(id=owner_object.id)==group_object.student:
                serializer=self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(status=HTTP_200_OK)
        return JsonResponse(
        {"errors": "User not a member of group"},
        status=400,
    )


    