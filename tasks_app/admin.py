from django.contrib import admin
from .models import Tasks,Notification, Location

#superuser
#superpwd

#employee1
#Red@1234

#employee2
#Red@1234
# Register your models here.

#Notification has been hidden to avoid overwriting
#admin.site.register(Notification)
admin.site.register(Tasks)
admin.site.register(Location)