from django.db import models

# Create your models here.
from enum import unique
from tkinter import CASCADE
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.
class PeopleList(models.Model):
    #id = models.PositiveIntegerField(primary_key=True)
    myself=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="myself")
    people=models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="people")

    USERNAME_FIELD="user"

    def add_people(self, account):
        if account not in self.people.all():
            if not (self.myself.is_student and account.is_student):
                self.people.add(account)
                self.save()

    def unfriend(self, account):
        removee=account
        if account in self.people:
            self.people.remove(removee)
            removee_friend_list=PeopleList.objects.get(myself=removee).first()
            removee_friend_list.people.remove(self.myself)

    def __str__(self):
        return self.myself.email