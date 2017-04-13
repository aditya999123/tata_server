from django.shortcuts import render

# Create your views here.
#initial_start=0
import time
from datetime import datetime as dt
#def generate_report(request):


def scheduler(hour1,hour2):
	
	flag=0
	print"triggered for sure"
	try:
		while(1):
			hour.dt.now().hour()
			if(flag==0 and hour==hour1):
				flag=1
				for o in add_user.models.dse_data.objects.all():
					o.tagret_achieved=False
					o.customer_reached_today=0
					o.save()
			
			if(hour!=hour1):
				flag=0

			if(hour>hour1 and hour<hour2):
				users.views.report_flag=False
			else:
				users.views.report_flag=True
			
			time.sleep(60*10)
	except:
		global initial_start
		initial_start=0
# @sched.scheduled_job('cron', day_of_week='mon-sun', hour=23)
# def scheduled_job1():
# 	email_summary()
# 	print('This job is run every weekday at 11pm.')
#if(initial_start==0):
print "triggered"
import multiprocessing as mp
p = mp.Process(target=scheduler,args=[6,18])
initial_start=1
p.start()