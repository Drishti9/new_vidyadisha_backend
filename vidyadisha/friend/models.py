from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import accounts.models
from twilio.rest import Client

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
                
                ###managing groups
                if self.myself.is_student:
                    #adding account to student group
                    student_obj=accounts.models.Student.objects.get(id=self.myself.id)
                    stu_group=Group.objects.filter(student=student_obj).first()
                    if not stu_group:
                        stu_group=Group.objects.create(student=student_obj)    
                    stu_group.add_member(account)

                    #updating group lists
                    g1=GroupList.objects.filter(person=self.myself).first()
                    g2=GroupList.objects.filter(person=account).first()
                    if not g1:
                        g1=GroupList.objects.create(person=self.myself)
                    if not g2:
                        g2=GroupList.objects.create(person=account)
                    g1.add_group(stu_group)
                    g2.add_group(stu_group)
                    

                # elif account.is_student:
                #     stu_group=Group.objects.filter(student=account).first()
                #     stu_group.add_member(self.myself)

    def unfriend(self, account):
        removee=account
        if account in self.people.all():
            self.people.remove(removee)
            removee_friend_list=FriendList.objects.filter(myself=removee).first()
            removee_friend_list.people.remove(self.myself)

            if self.myself.is_student:
                #removing account from student's group
                group=Group.objects.filter(student=self.myself).first()
                group.remove_member(account)

                #altering removee's group list
                group_list=GroupList.objects.filter(person=account).first()
                group_list.remove_group(group)

            elif account.is_student:
                #removing myself from student's group
                group=Group.objects.filter(student=account).first()
                group.remove_member(account)

                #altering remover's group list
                group_list=GroupList.objects.filter(person=self.myself).first()
                group_list.remove_group(group)


    def __str__(self):
        return str(self.myself)

class  FriendRequest(models.Model):
    sender=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")

    #is false when request accepted or declined
    isActive=models.BooleanField(null=False, default=True)

    timestamp=models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.sender.email

    def accept(self): 
        sender_friend_list=FriendList.objects.filter(myself=self.sender).first()
        if not sender_friend_list:
            sender_friend_list=FriendList.objects.create(myself=self.sender)
        sender_friend_list.add_friend(self.receiver)

        receiver_friend_list=FriendList.objects.filter(myself=self.receiver).first()
        if not receiver_friend_list:
            receiver_friend_list=FriendList.objects.create(myself=self.receiver)
        receiver_friend_list.add_friend(self.sender)
        
        self.isActive=False
        self.save()

    def decline(self, sender, receiver):
        self.isActive=False
        self.save()

class Group(models.Model):
    student=models.OneToOneField(accounts.models.Student, on_delete=models.CASCADE, related_name="student")
    members=models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="members")

    USERNAME_FIELD="student"

    def add_member(self, account):
        if not account.is_student:
            student_friend_list=FriendList.objects.filter(myself=self.student).first()
            if account in student_friend_list.people.all():
                self.members.add(account)
                self.save()

    def remove_member(self, account):
        if account in self.members.all():
            self.members.remove(account)
            self.save()

class GroupList(models.Model):
    person=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="person")
    group_list=models.ManyToManyField(Group, blank=True, related_name="groups")

    USERNAME_FIELD="myself"

    def add_group(self, group):
        if group not in self.group_list.all():
            self.group_list.add(group)
            self.save()

    def remove_group(self, group):
        if group in self.group_list.all():
            self.group_list.remove(group)
            self.save()

class Post(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owner")
    group=models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group")
    message=models.CharField(max_length=250)
    timestamp=models.DateTimeField(auto_now_add=True)



# class Score(models.Model):
#     #tutor, student, timestamp, result, subject
#     result=models.PositiveIntegerField()

#     def _str_(self):
#         return str(self.result)

#     def save(self,args,*kwargs):
#         if self.result <75 :
            
#             account_sid = 'ACbbc81ce39f850176d36eb33077b64e2c'
#             auth_token = '3ac9f36545703c5ee4c5fb8291a89858' 
#             client = Client(account_sid, auth_token) 
#             message = client.messages.create( 
#                             body = f"The current score is bad {self.result}",
#                             from_ = '+17755425836',
#                             to = '+919769004201' 
#                           )
#             print(message.sid) 
#         return super().save(args,*kwargs)

