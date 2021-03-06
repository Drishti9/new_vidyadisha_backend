from django.urls import path, include

from .models import *
from .views import *
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('friendlist/<int:pk>', FriendListViewSet.as_view(), name="friend-list"), #only get method
    path('unfriend/', UnfriendView.as_view(), name="unfriend"),#only post method
    path('friendrequest/', FriendRequestView.as_view(), name="friend-request"),#get:all user friend requests, post: any friend request
    path('friendrequestpending/<int:pk>', FriendRequestPendingView.as_view(), name="friend-request-pending"),#only get: sent requests, not accepted yet
    path('friendrequestacceptancepending/<int:pk>', FriendRequestAcceptancePendingView.as_view(), name="friend-request-acceptance-pending"),#only get: recieved requests, acceptance pending
    path('friendrequestaccept/', FriendRequestAcceptView.as_view(), name="friend-request-accept"),#only post: to post request for acceptance of friend request
    path('friendrequestdecline/', FriendRequestDeclineView.as_view(), name="friend-request-decline"),#only post: to post request for acceptance of friend request

    ###Group querying urls
    path('group/<int:pk>', GroupViewSet.as_view(), name="group"),#only get method, pk is group id
    path('grouplist/<int:pk>', GroupListViewSet.as_view(), name="group"),#only get method: all groups of person with id=pk 
    path('post/<int:pk>', PostGetViewSet.as_view(), name="post"), #only get: posts of group with id=pk
    path('post/', PostInsertViewSet.as_view(), name="post")#only post: new posts
    
]