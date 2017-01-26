from django.shortcuts import render
from keys.models import *
# Create your views here.
from add_user.models import dsm_data,dse_data,user_data

def view_dse(request):
	response={}

def view_dsm(request):
	respone={}
	try:
		access_token= request.POST.get("access_token")
		print "access_token :",access_token
		if access_token!=None:
			json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
			try:
				user=user_data.objects.get(user_name=json_decoded['user_name'])
				if(user.designation==0):
					tmp_array=[]
					for o in dsm_data.objects.all():
						tmp_json={}
						tmp['dsm_id']=o.id
						tmp['dsm_name']=user_data.objects.get(user_name=o.user_id).name
						tmp['image']=request.scheme+'://'+request.get_host()+'/media/'+str(user_data.objects.get(user_name=o.user_id).image)

					response['dsm_id']
				else:
					respone['success']=False
					respone['message']="insufficient access"
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

