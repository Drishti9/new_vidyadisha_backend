
from django.urls import path, include

from .models import *
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'subject', views.SubjectViewSet, basename='subject')
"""router.register(r'user', views.UserViewSet, basename='user')
router.register(r'student', views.StudentViewSet, basename='student')
router.register(r'tutor', views.TutorViewSet, basename='tutor')
router.register(r'donor', views.DonorViewSet, basename='donor')
router.register(r'mentor', views.MentorViewSet, basename='mentor')
router.register(r'stu-requiring-mentor', views.StuRequiringMentorViewSet, basename='stu-requiring-mentor')
router.register(r'stu-requiring-donor', views.StuRequiringDonorViewSet, basename='stu-requiring-donor')
router.register('stu-requiring-tutor', views.StuRequiringTutorViewSet, basename='stu-requiring-tutor')"""
"""
router.register('customuser', views.CustomUserViewSet, basename='customuser')
router.register('student', views.StudentAdditionalViewSet, basename='student')
router.register('mentor', views.MentorAdditionalViewSet, basename='mentor')
router.register('tutor', views.TutorAdditionalViewSet, basename='tutor')
router.register('donor', views.DonorAdditionalViewSet, basename='donor')
"""

user_list=views.UserViewSet.as_view({
        'get':'list',
        'post':'create'
    })

user_detail=views.UserViewSet.as_view({
        'get':'retrieve',
        'patch':'update',
        'delete':'destroy'
    })

student_list=views.StudentViewSet.as_view({
        'get':'list',
        'post':'create'
    })

student_detail=views.StudentViewSet.as_view({
        'get':'retrieve',
        'patch':'update',
        'delete':'destroy'
    })

mentor_list=views.MentorViewSet.as_view({
        'get':'list',
        'post':'create'
    })

mentor_detail=views.MentorViewSet.as_view({
        'get':'retrieve',
        'patch':'update',
        'delete':'destroy'
    })

tutor_list=views.TutorViewSet.as_view({
        'get':'list',
        'post':'create'
    })

tutor_detail=views.TutorViewSet.as_view({
        'get':'retrieve',
        'patch':'update',
        'delete':'destroy'
    })

donor_list=views.DonorViewSet.as_view({
        'get':'list',
        'post':'create'
    })

donor_detail=views.DonorViewSet.as_view({
        'get':'retrieve',
        'patch':'update',
        'delete':'destroy'
    })

stu_req_mentor_list=views.StuRequiringMentorViewSet.as_view({
        'get':'list',
        'post':'create'
    })

stu_req_donor_list=views.StuRequiringDonorViewSet.as_view({
        'get':'list',
        'post':'create'
    })
stu_req_tutor_list=views.StuRequiringTutorViewSet.as_view({
        'get':'list',
        'post':'create'
    })

urlpatterns = [
    path('', include(router.urls)),
    path('user/', views.UserInformation.as_view(), name="user_info"),
    path('user/<int:pk>', views.UserInformationWithId.as_view(), name="user_info_1"),
    path('student/',student_list, name="student-list"),
    path('student/<int:pk>',student_detail, name="student-detail"),
    path('mentor/',mentor_list, name="mentor-list"),
    path('mentor/<int:pk>',mentor_detail, name="mentor-detail"),
    path('tutor/',tutor_list, name="tutor-list"),
    path('tutor/<int:pk>',tutor_detail, name="tutor-detail"),
    path('donor/',donor_list, name="donor-list"),
    path('donor/<int:pk>',donor_detail, name="donor-detail"),
    path('user-register/', views.RegisterUser.as_view(), name="user-register"),
    path('student-register/', views.RegisterStudent.as_view(), name="student-register"),
    path('mentor-register/', views.RegisterMentor.as_view(), name="mentor-register"),
    path('donor-register/', views.RegisterDonor.as_view(), name="donor-register"),
    path('tutor-register/', views.RegisterTutor.as_view(), name="tutor-register"),
    path('stu-req-mentor/', stu_req_mentor_list, name="stu-requiring-mentor"),
    path('stu-req-tutor/', stu_req_tutor_list, name="stu-requiring-tutor"),
    path('stu-req-donor/', stu_req_donor_list, name="stu-requiring-donor"),
    path('login/', views.login_view, name="login"),
    path('sendemail/', views.sendemail, name="send email"),
    ]
    #path('logout/', views.logout_view, name="logout")
    # path('user/',user_list, name="user-list"),
    # path('user/<int:pk>',user_detail, name="user-detail"),
    #path('', include(router.urls)),
    #path('user-list/',views.UserList,name="User"),
    #path('student-list/',views.StudentList,name="Student"),
    #path('stucreate/', views.create_student, name='stucreate'),


"""    path('',views.apiOverview,name="apioverview"),
    path('custom-user-list/',views.CustomUserList,name="customUser"),
    path('custom-user-list/<str:pk>/',views.CustomUserDetail,name="customUser"),
    path('student-list/',views.StudentList,name="student"),
    path('mentor-list/',views.MentorList,name="mentor"),
    path('tutor-list/',views.TutorList,name="tutor"),
    path('donor-list/',views.DonorList,name="donor"),"""