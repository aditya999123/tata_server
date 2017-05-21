from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from .models import *
import hashlib
import jwt
from keys.models import KEYS_internal
from django.views.decorators.csrf import csrf_exempt
user_type_deg={0:'TSM',1:'DSM',2:'DSE'}

@csrf_exempt
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
					user=user_data.objects.get(id=json_decoded['user_id'])
					user_designation=int(user.designation)
					user_make_type=int(request.GET.get("user_make_type"))
					if(user.active==True):
						response['success']=True
						response['message']="all fine"
						print "user_designation",user_designation
						print "user_make_type",user_make_type
						if(user_designation==0 and user_make_type==1):
							tmp_array=[]
							for o in dealer_data.objects.all():
								tmp_json={}
								tmp_json['dealer_name']=o.name
								tmp_json['dealer_id']=o.id
								tmp_array.append(tmp_json)
							response['dealer_list']=tmp_array

						elif(user_designation==0 and user_make_type==2):
							tmp_array=[]
							#user_dsm=user_data.objects.get(id=dsm_id)
							for o in dsm_data.objects.all():#filter(dsm=user_dsm):
								tmp_json={}
								tmp_json['name']=o.user_id.name
								tmp_json['id']=o.user_id.id
								tmp_array.append(tmp_json)
							response['dsm_list']=tmp_array
						elif(user_designation==1):
							pass
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
					
					user=user_data.objects.get(id=json_decoded['user_id'])
					user_designation=int(user.designation)
					print "user_designation",user_designation
					if(user.active==True):
						try:
							print "@81"
							user_make_type=int(request.POST.get("user_make_type"))
							print "user_make_type",user_make_type

							if(user_make_type<=user_designation):
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
										if(user_make_type==1):
											dealer_id=request.POST.get('choose_id')
											dealer=dealer_data.objects.get(id=dealer_id)
											user_tsm=tsm_data.objects.get(user_id=user)
											dsm_data.objects.create(user_id=new_user,tsm=user_tsm,dealer=dealer)
											new_user.designation=1
											new_user.save()
										if(user_make_type==2 and user_designation==1):
											# dealer_id=request.POST.get('choose_id')
											# dealer=dealer_data.objects.get(id=dealer_id)
											user_dsm=dsm_data.objects.get(user_id=user)
											dse_data.objects.create(user_id=new_user,dsm=user_dsm)
											new_user.designation=2
											new_user.save()
										if(user_make_type==2 and user_designation==0):
											dsm_id=request.POST.get('choose_id')
											user_dsm=user_data.objects.get(id=dsm_id)
											dsm_user=dsm_data.objects.get(user_id=user_dsm)
											dse_data.objects.create(user_id=new_user,dsm=dsm_user)
											new_user.designation=2
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
	print response
	return JsonResponse(response)

@csrf_exempt
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
				response['user_type']=user.designation
				response['user_id']=user.id
				response['access_token']=jwt.encode({'user_id':user.id}, str(KEYS_internal.objects.get(key='jwt').value), algorithm='HS256')

				if user.first_time_user==True:
					response['change_password']=True
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
	print response
	return JsonResponse(response)

@csrf_exempt
def change_password(request):
	response={}
	try:
		access_token= request.POST.get("access_token")
		print "access_token :",access_token
		if access_token!=None:
			json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
			try:
				user=user_data.objects.get(id=json_decoded['user_id'])
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