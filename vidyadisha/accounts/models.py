from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import *

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=40, blank=True)
    last_name = models.CharField(_("last name"), max_length=40, blank=True)
    mobile = models.CharField(_("mobile"), max_length=13, blank=True)
    address = models.CharField(_("address"), max_length=255, blank=True)
    # date_joined = models.DateTimeField(_('date joined'), auto_now_add = True)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_superuser = models.BooleanField(_("is superuser"), default=False)
    is_admin = models.BooleanField(_("is admin"), default=False)
    is_student = models.BooleanField(_("is student"), default=False)
    is_mentor = models.BooleanField(_("is teacher"), default=False)
    is_tutor = models.BooleanField(_("is librarian"), default=False)
    is_donor = models.BooleanField(_("is librarian"), default=False)
    objects = UserManager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]

    class Meta:
        verbose_name=_("user")
        verbose_name_plural=_("users")

    def save(self, *args, **kwargs):
        self.username = self.email
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class Student(User):
    user=models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    user.is_student=True
    user.is_mentor=False
    user.is_tutor=False
    user.is_donor=False

    standard=models.IntegerField()
    institute=models.CharField(max_length=200, null=True)
    requiresDonation=models.BooleanField(default=True)
    requiresMentor=models.BooleanField(default=True)
    requiresTutor=models.BooleanField(default=True)

    objects=StudentManager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["standard", "institute"]

    def __str__(self):
        return self.user.email


class Mentor(User):
    user=models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    user.is_student=False
    user.is_mentor=True
    user.is_tutor=False
    user.is_donor=False

    occupation=models.CharField(max_length=300)

    objects=MentorManager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["occupation"]

    def __str__(self):
        return self.user.email

class Subject(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Tutor(User):
    user=models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    user.is_student=False
    user.is_mentor=False
    user.is_tutor=True
    user.is_donor=False

    experience_in_years=models.IntegerField()
    subject=models.ManyToManyField(Subject,  related_name="tutors")

    objects=TutorManager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["subject"]

    def __str__(self):
        return self.user.email

class Donor(User):
    user=models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    user.is_student=False
    user.is_mentor=False
    user.is_tutor=False
    user.is_donor=True

    DONATION_TYPE=(
        ('monthly','monthly'),
        ('annual','annual'),
    )
    donation_type=models.CharField(max_length=50,choices=DONATION_TYPE)

    objects=DonorManager()

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["donation_type"]

    def __str__(self):
        return self.user.email