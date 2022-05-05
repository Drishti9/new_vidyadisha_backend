from enum import unique
from xml.parsers.expat import model
#from tkinter import CASCADE
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from accounts.models import Student

# Create your models here.
class FriendList(models.Model):
    #id = models.PositiveIntegerField(primary_key=True)
    myself=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="myself")
    people=models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="people")

    USERNAME_FIELD="myself"

    def add_friend(self, account): ####TO BE DONE: handle providing permissions to added users
        if account not in self.people.all() and self.myself!=account:
            if not (self.myself.is_student and account.is_student):
                self.people.add(account)
                self.save()

    def unfriend(self, account):
        removee=account
        if account in self.people.all():
            self.people.remove(removee)
            removee_friend_list=FriendList.objects.filter(myself=removee).first()
            removee_friend_list.people.remove(self.myself)

        """if self.myself.is_student:
            #removing account from student's group
            group=Group.objects.filter(student=self.myself).first()
            group.remove_member(account)

            #altering removee's group list
            group_list=GroupList.objects.filter(person=account).first()
            group_list.remove_group(group)"""

    def __str__(self):
        return self.myself.id

class  FriendRequest(models.Model):
    sender=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")

    #is false when request accepted or declined
    isActive=models.BooleanField(null=False, default=True)

    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.email

    def accept(self): 
        sender_friend_list=FriendList.objects.get(myself=self.sender)
        if sender_friend_list:
            sender_friend_list.add_friend(self.receiver)
            receiver_friend_list=FriendList.objects.get(myself=self.receiver)
            receiver_friend_list.add_friend(self.sender)
            self.isActive=False
            self.save()

    def decline(self, sender, receiver):
        self.isActive=False
        self.save()

"""class Group(models.Model):
    student=models.OneToOneField(Student, on_delete=models.CASCADE, related_name="student")
    members=models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="members")

    USERNAME_FIELD="student"

    def add_member(self, account):
        if not account.is_student:
            student_friend_list=FriendList.objects.filter(myself=self.student).first()
            if account in student_friend_list.people:
                self.people.add(account)
                self.save()

    def remove_member(self, account):
        if account in self.members:
            self.members.remove(account)
            self.save()

class GroupList(models.Model):
    person=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="person")
    group_list=models.ManyToManyField(Group, blank=True, related_name="groups")

    USERNAME_FIELD="myself"

    def add_group(self, group):
        if group not in self.group_list:
            self.group_list.add(group)
            self.save()

    def remove_group(self, group):
        if group in self.group_list:
            self.group_list.remove(group)
            self.save()"""