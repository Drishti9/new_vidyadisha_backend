from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework import generics

from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

# Create your views here.
class FriendListViewSet(generics.GenericAPIView):
    http_method_names = ["get"]

    serializer_class = FriendListSerializer
    queryset = FriendList.objects.all()

    def get(self, request, pk):
        myself_object=get_user_model().objects.get(id=pk)
        tuples = FriendList.objects.filter(myself=myself_object)
        serializer = FriendListSerializer(tuples, many=True)
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

    def post(self, request, pk):
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


