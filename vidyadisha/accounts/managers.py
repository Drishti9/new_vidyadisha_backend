from django.contrib.auth.base_user import BaseUserManager
import accounts.models
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        user = self.create_user(
        email=self.normalize_email(email),
        password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class StudentManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        standard,
        institute,
        requiresDonation,
        requiresMentor,
        requiresTutor,
        password=None,
        **extra_fields
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user=self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            standard=standard,
            institute=institute,
            requiresDonation=requiresDonation,
            requiresMentor=requiresMentor,
            requiresTutor=requiresTutor,
            is_student=True,
            is_mentor=False,
            is_tutor=False,
            is_donor=False,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class MentorManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        occupation,
        password=None,
        **extra_fields
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user=self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            occupation=occupation,
            is_student=False,
            is_mentor=True,
            is_tutor=False,
            is_donor=False,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class TutorManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        experience_in_years,
        password=None,
        **extra_fields
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user=self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            experience_in_years=experience_in_years,
            is_student=False,
            is_mentor=False,
            is_tutor=True,
            is_donor=False,
            **extra_fields
        )
        user=accounts.models.Tutor(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            experience_in_years=experience_in_years,
            is_student=False,
            is_mentor=False,
            is_tutor=True,
            is_donor=False,
        )    

        """x=set()
        for each in subjects:
            s=accounts.models.Subject.objects.filter(name=each.lower()).first()
            if not s:
                s=accounts.models.Subject.objects.create(name=each)
            x.add(s.pk)

        subs=accounts.models.Subject.objects.filter(pk__in=x)
        user.__setattr__(subject=subs)"""

        """
        x=set()
        for each in subjects:
            s=accounts.models.Subject.objects.filter(name=each.lower()).first()
            if not s:
                s=accounts.models.Subject.objects.create(name=each)
            #self.model.subject.append()

        """
        #user(subject=subs)

        user.set_password(password)
        user.save(using=self._db)
        return user

class DonorManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        donation_type,
        password=None,
        **extra_fields
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user=self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            is_student=False,
            is_mentor=False,
            is_tutor=False,
            is_donor=True,
            donation_type=donation_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user