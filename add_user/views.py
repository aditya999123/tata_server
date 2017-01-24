from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from .models import *

def add_user_fun(request):
	respone={}
	if request.method=='GET':
		try:
			pass


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