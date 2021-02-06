
from django.urls import path
from .import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.home, name = 'home'),
    path('home', views.home, name = 'home'),
    path('login', views.login, name = 'login'),
    path('user_login', views.user_login, name = 'user_login'),
    path('logout', views.logout, name = 'logout'),
    path('signup',views.signup, name = 'signup'),
    path('user_registration', views.user_registration, name = 'user_registration'),
    path('task',views.task, name = 'task'),
    path('taskupdate', views.taskupdate, name = 'taskup'),
    path('add_task', views.add_task, name = 'add_task'), 
    path('notification', views.notification, name = 'notification'),
    path('delete', views.delete, name = 'delete')
]