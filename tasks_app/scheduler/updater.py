from apscheduler.schedulers.background import BackgroundScheduler
from tasks_app.views import taskfile

#Function to save tasks on weekly basis, this function is called by apps.ready()
def start():
    scheduler = BackgroundScheduler()
    task = taskfile()
    scheduler.add_job(task.savefile,'cron',day_of_week = 'sun', hour = 9, minute = 30, id='task001', replace_existing=True)
    scheduler.start()