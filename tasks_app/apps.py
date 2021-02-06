from django.apps import AppConfig


class TasksAppConfig(AppConfig):
    name = 'tasks_app'

    def ready(self):
        #Calling Updater function to set up and send save task file on a weekly basis
        from .scheduler import updater
        updater.start()
