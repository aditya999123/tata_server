from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from .models import *
import hashlib
import jwt
from keys.models import KEYS_internal
user_type_deg={0:'TSM',1:'DSM',2:'DSE'}

def add_user_fun(request):
	response={}
	#####################################################################################
	if request.method=='GET':
		try:
			access_token= request.GET.get("access_token")
			print "access_token :",access_token
			if access_token!=None:
				#print "key:",str(KEYS_internal.objects.get(key='jwt').value)
				json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
				try:
					user=user_data.objects.get(user_name=json_decoded['user_name'])
					user_designation=user.designation
					if(user.active==True):
						if(user_designation==0):
							tmp_array=[]
							for o in dsm_data.objects.all():
								tmp_json={}
								tmp_json['name']=user_data.objects.get(user_name=o.user_id).name
								tmp_json['id']=o.id
								tmp_array.append(tmp_json)
							response['dsm_list']=tmp_array
						else:
							response['success']=False
							response['insufficient access']
					else:
						response['success']=False
						response['Access Denied']
				except Exception,e:
					response['success']=False
					response['message']=str(e)
			else:
				response['success']=False
				response['message']="No Access token recieved"
		except Exception,e:
			response['success']=False
			response['message']=str(e)
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
					if(user.active==True):
						try:

							user_type_make=int(request.POST.get("user_type"))
							print "user to be added deg",user_type

							if(user_type_make<=user_type_deg[user_designation]):
								response['success']=False
								response['message']='access denied'
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
											new_user.designation=1
											new_user.save()
										if(user_type_make==2 and user_designation==1):
											dse_data.objects.create(user_id=new_user,dsm=user)
											new_user.designation=2
											new_user.save()
										if(user_type_make==2 and user_designation==0):
											dsm_id=request.POST.get('dsm_id')
											dse_data.objects.create(user_id=new_user,dsm=dsm_data.objects.get(id=int(dsm_id)))
											new_user.designation==2
											new_user.save()
										response['success']=True
										response['password']='abcd'
										response['message']='Successful'
									else:
										response['success']=False
										response['message']='user with this username already exsists'
								except Exception,e:
									response['success']=False
									response['message']=str(e)
						except Exception,e:
							response['success']=False
							response['message']=str(e)
					else:
						response['success']=False
						response['message']='access denied'
				except Exception,e:
					response['success']=False
					response['message']=str(e)
			else:
				response['success']=False
				response['message']="No Access token recieved"
		except Exception,e:
			response['success']=False
			response['message']=str(e)

	return JsonResponse(response)

def login(request):
	response={}
	try:
		user_name=request.POST.get("user_name")
		password=hashlib.sha512(request.POST.get("password")).hexdigest().lower()
		user=user_data.objects.get(user_name=user_name)
		if(user.active==True):
			if(user.password==password):
				response['success']=True
				response['message']="Successfull"

				if user.first_time_user==True:
					response['change_password']=True
					response['user_designation']=user.designation
					response['access_token']=jwt.encode({'user_name':user_name}, str(KEYS_internal.objects.get(key='jwt').value), algorithm='HS256')
					user.first_time_user=False
					user.save()
				else:
					response['change_password']=False
			else:
				response['success']=False
				response['message']="Password did not match"
		else:
			response['success']=False
			response['message']='Access Denied'
	except Exception,e:
		response['success']=False
		response['message']=str(e)
	return JsonResponse(response)

def change_password(request):
	response={}
	try:
		access_token= request.POST.get("access_token")
		print "access_token :",access_token
		if access_token!=None:
			json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
			try:
				user=user_data.objects.get(user_name=json_decoded['user_name'])
				if(user.active==True):
					password=hashlib.sha512(request.POST.get("password")).hexdigest().lower()
					new_password=hashlib.sha512(request.POST.get("new_password")).hexdigest().lower()
					if(user.password==password):
						response['success']=True
						response['message']="Successfull"
						user.password=new_password
						user.save()
					else:
						response['success']=False
						response['message']="initial Password did not match"
				else:
					response['success']=False
					response['message']="access Denied"
			except Exception,e:
				response['success']=False
				response['message']=str(e)

		else:
			response['success']=False
			response['message']='no access token'
	except Exception,e:
		response['success']=False
		response['message']=str(e)
		
	return JsonResponse(response)