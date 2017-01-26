from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from .models import *
import hashlib
import jwt
from keys.models import KEYS_internal
user_type_deg={0:'TSM',1:'DSM',2:'DSE'}

def add_user_fun(request):
	respone={}
	#####################################################################################
	if request.method=='GET':
		try:
			access_token= request.GET.get("access_token")
			print "access_token :",access_token
			if access_token!=None:
				#print "key:",str(KEYS_internal.objects.get(key='jwt').value)
				json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
				try:
					user_designation=user_data.objects.get(user_name=json_decoded['user_name']).designation
					if(user_designation==0):
						tmp_array=[]
						for o in dsm_data.objects.all():
							tmp_json={}
							tmp_json['name']=user_data.objects.get(user_name=o.user_id).name
							tmp_json['id']=o.id
							tmp_array.append(tmp_json)
						respone['dsm_list']=tmp_array
					else:
						respone['success']=False
						respone['insufficient access']
				except Exception,e:
					respone['success']=False
					respone['message']=str(e)
			else:
				respone['success']=False
				respone['message']="No Access token recieved"
		except Exception,e:
			respone['success']=False
			respone['message']=str(e)
	####################################33333#############################################
	if request.method=='POST':
		try:
			access_token= request.POST.get("access_token")
			print "access_token :",access_token
			if access_token!=None:
				#print "key:",str(KEYS_internal.objects.get(key='jwt').value)
				json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
				try:
					
					user=user_data.objects.get(user_name=json_decoded['user_name'])
					user_designation=user.designation
					try:

						user_type_make=int(request.POST.get("user_type"))
						print "user to be added deg",user_type

						if(user_type_make<=user_type_deg[user_designation]):
							respone['success']=False
							respone['message']='access denied'
						else:
							try:
								name=request.POST.get('name')
								user_name=request.POST.get('user_name')
								print "name and user_name recieved",name,user_name
								new_user,created=user_data.objects.get_or_create(user_name=user_name)
								if created==True:
									new_user.name=name
									new_user.save()
									if(user_type_make==1):
										dsm_data.objects.create(user_id=new_user,tsm=user)
									if(user_type_make==2 and user_designation==1):
										dse_data.objects.create(user_id=new_user,dsm=user)
									if(user_type_make==2 and user_designation==0):
										dsm_id=request.POST.get('dsm_id')
										dse_data.objects.create(user_id=new_user,dsm=dsm_data.objects.get(id=int(dsm_id)))
									respone['success']=True
									respone['password']='abcd'
									respone['message']='Successful'
								else:
									respone['success']=False
									respone['message']='user with this username already exsists'
							except Exception,e:
								respone['success']=False
								respone['message']=str(e)
					except Exception,e:
						respone['success']=False
						respone['message']=str(e)
				except Exception,e:
					respone['success']=False
					respone['message']=str(e)
			else:
				respone['success']=False
				respone['message']="No Access token recieved"
		except Exception,e:
			respone['success']=False
			respone['message']=str(e)

	return JsonResponse(respone)

def login(request):
	respone={}
	try:
		user_name=request.POST.get("user_name")
		password=hashlib.sha512(request.POST.get("password")).hexdigest().lower()
		user=user_data.objects.get(user_name=user_name)
		if(user.password==password):
			respone['success']=True
			respone['message']="Successfull"

			if user.first_time_user==True:
				respone['change_password']=True
				respone['user_designation']=user.designation
				respone['access_token']=jwt.encode({'user_name':user_name}, str(KEYS_internal.objects.get(key='jwt').value), algorithm='HS256')
				user.first_time_user=False
				user.save()
			else:
				respone['change_password']=False
		else:
			respone['success']=False
			respone['message']="Password did not match"
	except Exception,e:
		respone['success']=False
		respone['message']=str(e)
	return JsonResponse(respone)

def change_password(request):
	respone={}
	try:
		access_token= request.POST.get("access_token")
		print "access_token :",access_token
		if access_token!=None:
			json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
			try:
				user=user_data.objects.get(user_name=json_decoded['user_name'])
				password=hashlib.sha512(request.POST.get("password")).hexdigest().lower()
				new_password=hashlib.sha512(request.POST.get("new_password")).hexdigest().lower()
				if(user.password==password):
					respone['success']=True
					respone['message']="Successfull"
					user.password=new_password
					user.save()
				else:
					respone['success']=False
					respone['message']="initial Password did not match"
			except Exception,e:
				respone['success']=False
				respone['message']=str(e)

		else:
			respone['success']=False
			respone['message']='no access token'
	except Exception,e:
		respone['success']=False
		respone['message']=str(e)
		
	return JsonResponse(respone)