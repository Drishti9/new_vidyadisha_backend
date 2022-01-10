
from django.urls import path, include

from .models import *
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', views.UserViewSet, basename='user')
router.register('student', views.StudentViewSet, basename='student')
router.register('tutor', views.TutorViewSet, basename='tutor')
router.register('donor', views.DonorViewSet, basename='donor')
router.register('mentor', views.MentorViewSet, basename='mentor')
router.register('stu-requiring-mentor', views.StuRequiringMentorViewSet, basename='stu-requiring-mentor')
router.register('stu-requiring-donor', views.StuRequiringDonorViewSet, basename='stu-requiring-donor')
router.register('stu-requiring-tutor', views.StuRequiringTutorViewSet, basename='stu-requiring-tutor')
"""
router.register('customuser', views.CustomUserViewSet, basename='customuser')
router.register('student', views.StudentAdditionalViewSet, basename='student')
router.register('mentor', views.MentorAdditionalViewSet, basename='mentor')
router.register('tutor', views.TutorAdditionalViewSet, basename='tutor')
router.register('donor', views.DonorAdditionalViewSet, basename='donor')
"""
urlpatterns = [
    path('', include(router.urls)),
    path('user-register', views.RegisterUser.as_view(), name="user-register"),
    path('student-register', views.RegisterStudent.as_view(), name="student-register"),
    path('mentor-register', views.RegisterMentor.as_view(), name="mentor-register"),
    path('donor-register', views.RegisterDonor.as_view(), name="donor-register"),
    path('tutor-register', views.RegisterTutor.as_view(), name="tutor-register"),
    #path('user-list/',views.UserList,name="User"),
    #path('student-list/',views.StudentList,name="Student"),
    #path('stucreate/', views.create_student, name='stucreate'),
]

"""    path('',views.apiOverview,name="apioverview"),
    path('custom-user-list/',views.CustomUserList,name="customUser"),
    path('custom-user-list/<str:pk>/',views.CustomUserDetail,name="customUser"),
    path('student-list/',views.StudentList,name="student"),
    path('mentor-list/',views.MentorList,name="mentor"),
    path('tutor-list/',views.TutorList,name="tutor"),
    path('donor-list/',views.DonorList,name="donor"),"""