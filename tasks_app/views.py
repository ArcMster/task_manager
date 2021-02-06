from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import Tasks, Notification, Location
from django.http import HttpResponse, JsonResponse
from .serializers import TaskSerializer
from collections import ChainMap
import datetime, json
import pandas as pd
from django.contrib.auth.models import User, auth



#Class based view working Django-rest framework to save the tasks in an excelsheet (Scheduler.Updater.start is the function which calls taskfile to save tasks in excel sheet).
class taskfile(APIView):
    def savefile(self):
        
        days = datetime.timedelta(5)
        filter_limit = datetime.datetime.now() - days
        current_tasks = Tasks.objects.filter(time__gt = filter_limit)
        outdict = {'Employee': [],'Task': [], 'Time': []}
        for i in current_tasks:
            
            outdict['Employee'].append(i.employee.username)
            outdict['Task'].append(i.task)
            outdict['Time'].append(str(i.time.strftime("%Y-%m-%d %H:%M:%S")))
        outputdf = pd.DataFrame(outdict)
        locations = Location.objects.values('location')
        print(locations)
        for i in locations:
            file_name = i['location'] + "\\Tasks" + datetime.datetime.today().strftime("%d%m%Y") + ".xlsx"
            outputdf.to_excel(file_name)
        return 



#Function based view to send notification to superuser during create/update event of a task
def notification(request):
    check = Notification.objects.get(id = 1)
    employee = Notification.objects.values('employee')
    active_user =User.objects.get(id = employee[0]['employee'])
    
    if check.notification_state == 'Active' and request.user.username!= str(active_user):
        check.notification_state = 'Inactive'
        check.save()
        return JsonResponse({'check': 'true', 'employee': str(active_user)})
        
    else:
        return JsonResponse({'check': 'false'})



#Function based view to display home/task page. It automatically routes to login page if user is not authenticated
def home(request):
    if request.user.is_authenticated:
        return redirect('task')
    else:
        return redirect('login')

#Function based view to load login page
def login(request):
    return render(request,'login.html')



#Function based view to display task page where all tasks will be displayed
def task(request):
    if request.user.is_authenticated:
        user = request.user
        if request.user.is_superuser:
            tasks = Tasks.objects.all()
        else:
            tasks = Tasks.objects.filter(employee=user)
        print(tasks)
        return render(request,'task.html',{'tasks': tasks})
    else:
        return redirect('login')



#Function based view to update an existing task by Django-rest framework
def taskupdate(request):
    task = Tasks.objects.get(id = int(request.POST['id']))
    task.task = request.POST['task']
    task.time = timeformat(request.POST['time'])
    if request.user.is_superuser:
        task.comments = request.POST['comment']

    task.save()
    check = Notification.objects.get(id = 1)
    check.employee = request.user
    check.notification_state = 'Active'
    check.save()
    
    return JsonResponse({'value': "Success"})



#Function based view to add a new task by Django-rest framework
def add_task(request):
    new_task = Tasks()
    new_task.task = request.POST['task']
    new_task.time = timeformat(request.POST['time'])
    new_task.employee = request.user
    new_task.save()
    check = Notification.objects.get(id = 1)
    check.employee = request.user
    check.notification_state = 'Active'
    check.save()
    id = Tasks.objects.last().id
    
    return JsonResponse({'value': 'task added','id': id})



#Function to format date-time to a format which can stored in database
def timeformat(time):
    datetime = ""
    splitime = time.split('T')
    datetime = splitime[0] + " " + splitime[1]
    return datetime




#Functon based view for login by Django-rest framework
def user_login(request):
    user_name = request.POST['userid']
    user_password = request.POST['password']
    user = auth.authenticate(username = user_name,password= user_password)
    if user is not None:
        
        auth.login(request,user)
        #return redirect('home')
        return JsonResponse({'value': 'valid'})
    else:
        
        return JsonResponse({'value': 'invalid'})



#Function based view to logout a user
def logout(request):
    auth.logout(request)
    return redirect('home')



#Function based view to load signup page
def signup(request):
    return render(request,'signup.html')



#Function based view to create a new user by Django-rest framework
def user_registration(request):
    
    uname = request.POST['uname']
    f_name = request.POST['f_name']
    l_name = request.POST['l_name']
    email = request.POST['email']
    passwd = request.POST['passwd']
    if User.objects.filter(username = uname).exists():
        return JsonResponse({'value':'username_exists'})
    elif User.objects.filter(email = email).exists():
        return JsonResponse({'value': 'email_exists'})
    else:
        user = User.objects.create_user(username = uname, first_name = f_name, last_name = l_name, email = email, password = passwd)
        user.save()
        return JsonResponse({'value': 'user_created'})




#Function based view to delete a task by Django-rest framework
def delete(request):
    Tasks.objects.get(id = request.POST['id']).delete()
    check = Notification.objects.get(id = 1)
    check.employee = request.user
    check.notification_state = 'Active'
    check.save()
    return JsonResponse({'response': 'deleted'})
