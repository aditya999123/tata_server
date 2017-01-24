from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from .models import *

def add_user_fun(request):
	respone={}
	if request.method=='GET':
		try:
			data=[]
			for o in user_level.objects.all():
				tmp_json={}
				tmp_json['user_level']=o.user_level
				tmp_json['name']=o.name
				data.append(tmp_json)
			respone['data']=data
		except Exception,e:
			respone['success']=False
			respone['message']=str(e)
	if request.method=='POST':
		try:
			pass
		except Exception,e:
			respone['success']=False
			respone['message']=str(e)

	return JsonResponse(respone)