from django.urls import path, include

from .models import *
from .views import *
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('friendlist/', FriendListViewSet.as_view(), name="friend-list"),
    path('unfriend/', UnfriendView.as_view(), name="unfriend"),
    path('friendrequest/', FriendRequestView.as_view(), name="friend-request"),
    path('friendrequestaccept/', FriendRequestAcceptView.as_view(), name="friend-request-accept"),
    path('friendrequestdecline/', FriendRequestDeclineView.as_view(), name="friend-request-decline"),   
]