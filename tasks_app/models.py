from django.db import models
from django.contrib.auth.models import User


#Function to edit User table
def get_user_name(self):
    return self.username

User.add_to_class("__str__", get_user_name)

#Model to store tasks
class Tasks(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    time = models.DateTimeField()
    comments = models.CharField(max_length=255, blank=True)

    class Meta():
        verbose_name_plural = 'Tasks'

#Choices for notification
state_choices = (
    ('Active','Active'),
    ('Inactive','Inactive')
)

#Model for sending notification, it stores the state(Active/Inactive) and the user who has made the last update
class Notification(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_state = models.CharField(max_length=10, choices=state_choices, default='Inactive')

#Model to store the location of the excel file on a weekly basis
class Location(models.Model):
    location = models.CharField(max_length=255)



