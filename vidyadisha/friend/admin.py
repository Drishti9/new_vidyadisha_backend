from django.contrib import admin

# Register your models here.
from .models import *

class FriendRequestAdmin(admin.ModelAdmin):
    search_fields=['sender', 'reciever']
    list_display=['sender', 'reciever']
    list_filter=['sender', 'reciever']

    class Meta:
        model=FriendRequest

"""class FriendListAdmin(admin.ModelAdmin):
    list_display=['myself', 'people']
    
    class Meta:
        model=FriendList"""

admin.site.register(FriendList)
admin.site.register(FriendRequest)