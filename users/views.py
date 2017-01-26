from django.shortcuts import render
from keys.models import *
# Create your views here.
from add_user.models import dsm_data,dse_data,user_data

def view_dsm(request):
	response={}
	try:
		access_token= request.POST.get("access_token")
		print "access_token :",access_token
		if access_token!=None:
			json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
			try:
				user=user_data.objects.get(user_name=json_decoded['user_name'])
				if(user.active==True):
					if(user.designation==0):
						tmp_array=[]
						for o in dsm_data.objects.filter(tsm=user.user_name):
							tmp_json={}
							tmp['dsm_id']=o.id
							user_in_list=user_data.objects.get(user_name=o.user_id)
							tmp['dsm_name']=user_in_list.name
							tmp['dsm_user_name']=user_in_list.user_name
							tmp['image']=request.scheme+'://'+request.get_host()+'/media/'+str(user_in_list.image)
							tmp_array.append(tmp_json)

						response['dsm_list']=tmp_array
					else:
						response['success']=False
						response['message']="insufficient access"
				else:
					response['success']=False
					response['message']="Access Denied"
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

def view_dse(request):
	response={}
	try:
		access_token= request.POST.get("access_token")
		print "access_token :",access_token
		if access_token!=None:
			json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
			try:
				user=user_data.objects.get(user_name=json_decoded['user_name'])
				if(user.active==True):
					if(user.designation==0):
						dsm_id=int(request.GET.get('dsm_id'))
						tmp_array=[]
						dsm_user_name=dsm_data.objects.get(id=dsm_id).user_id
						for o in dse_data.objects.filter(dsm=dsm_user_name):
							tmp_json={}
							tmp['dse_id']=o.id
							user_in_list=user_data.objects.get(user_name=o.user_id)
							tmp['dse_name']=user_in_list.name
							tmp['dse_user_name']=user_in_list.user_name
							tmp['image']=request.scheme+'://'+request.get_host()+'/media/'+str(user_in_list.image)
							tmp_array.append(tmp_json)

					if(user.designation==1):
						tmp_array=[]
						for o in dse_data.objects.filter(dsm=user.user_name):
							tmp_json={}
							tmp['dse_id']=o.id
							user_in_list=user_data.objects.get(user_name=o.user_id)
							tmp['dse_name']=user_in_list.name
							tmp['dse_user_name']=user_in_list.user_name
							tmp['image']=request.scheme+'://'+request.get_host()+'/media/'+str(user_in_list.image)
							tmp_array.append(tmp_json)

						response['dsm_list']=tmp_array
					else:
						response['success']=False
						response['message']="insufficient access"
				else:
					response['success']=False
					response['message']='Access Denied'
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
user_type_deg={0:'TSM',1:'DSM',2:'DSE'}
def view_profile(request):
	response={}
	if request.method=='GET':
		try:
			access_token= request.POST.get("access_token")
			print "access_token :",access_token
			if access_token!=None:
				json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
				try:
					user=user_data.objects.get(user_name=json_decoded['user_name'])
					if(user.active==True):
						user_name_profile=request.GET.get('user_name_profile')
						if(user_name_profile==None):
							user_name_profile=user.user_name
						user_profile=user_data.objects.get(user_name=user_name_profile)
						tmp_json={}
						tmp['name']=user_profile.name
						tmp['user_name']=user_profile.user_name
						tmp['mobile']=user_profile.mobile
						tmp['image']=request.scheme+'://'+request.get_host()+'/media/'+str(user_profile.image)
						tmp['address']=request.scheme+'://'+request.get_host()+'/media/'+str(user_profile.image)
						tmp['designation']=user_type_deg[user_profile.designation]
						tmp['profile']=user_profile.profile
						#tmp_array.append(tmp_json)

						response['profile_data']=tmp_json
					else:
						response['success']=False
						response['message']="Access Denied"

				except Exception,e:
					response['success']=False
					response['message']=str(e)

			else:
				response['success']=False
				response['message']='no access token'
		except Exception,e:
			response['success']=False
			response['message']=str(e)

	if request.message=='POST':
		try:
			access_token= request.POST.get("access_token")
			print "access_token :",access_token
			if access_token!=None:
				json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
				try:
					user=user_data.objects.get(user_name=json_decoded['user_name'])
					user_name_profile=request.GET.get('user_name_profile')
					if(user_name_profile==None):
						user_name_profile=user.user_name
					user_profile=user_data.objects.get(user_name=user_name_profile)
					tmp_json={}
					tmp['name']=user_profile.name
					tmp['user_name']=user_profile.user_name
					tmp['mobile']=user_profile.mobile
					tmp['image']=request.scheme+'://'+request.get_host()+'/media/'+str(user_profile.image)
					tmp['address']=user_profile.address
					tmp['designation']=user_type_deg[user_profile.designation]
					tmp['profile']=user_profile.profile
					#tmp_array.append(tmp_json)

					response['profile_data']=tmp_json

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
