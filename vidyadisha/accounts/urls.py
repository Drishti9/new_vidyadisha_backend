
from django.urls import path, include

from .models import *
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
"""
router.register('customuser', views.CustomUserViewSet, basename='customuser')
router.register('student', views.StudentAdditionalViewSet, basename='student')
router.register('mentor', views.MentorAdditionalViewSet, basename='mentor')
router.register('tutor', views.TutorAdditionalViewSet, basename='tutor')
router.register('donor', views.DonorAdditionalViewSet, basename='donor')
"""
urlpatterns = [
    path('', include(router.urls)),
    #path('stucreate/', views.create_student, name='stucreate'),
]

"""    path('',views.apiOverview,name="apioverview"),
    path('custom-user-list/',views.CustomUserList,name="customUser"),
    path('custom-user-list/<str:pk>/',views.CustomUserDetail,name="customUser"),
    path('student-list/',views.StudentList,name="student"),
    path('mentor-list/',views.MentorList,name="mentor"),
    path('tutor-list/',views.TutorList,name="tutor"),
    path('donor-list/',views.DonorList,name="donor"),"""