from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from .models import *
import hashlib
import json
import jwt
from keys.models import KEYS_internal
from django.views.decorators.csrf import csrf_exempt
from add_user.models import *
user_type_deg={0:'TSM',1:'DSM',2:'DSE'}
import datetime
@csrf_exempt
def add_customer(request):
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
					response['user_list']=[]
					if user_designation==0:
						for o in dse.objects.all():
							tmp_json={}
							tmp_json['name']=o.user_id.name+' - '+o.dsm.user_id.name
							tmp_json['id']=o.id
							response['user_list'].append(tmp_json)
					
					if user_designation==1:
						for o in dse.objects.filter(dsm=user):
							tmp_json={}
							tmp_json['name']=o.user_id.name
							tmp_json['id']=o.id
							response['user_list'].append(tmp_json)

					response['district_list']=[]
					for o in district_data.objects.all():
						tmp_json={}
						tmp_json['id']=o.id
						tmp_json['name']=o.name
						response['district_list'].append(tmp_json)
					
					response['town_list']=[]
					for o in town_data.objects.all():
						tmp_json={}
						tmp_json['id']=o.id
						tmp_json['name']=o.name
						response['town_list'].append(tmp_json)
					
					response['vehicle_list']=[]
					for o in vehicle_data.objects.all():
						tmp_json={}
						tmp_json['id']=o.id
						tmp_json['name']=o.name
						response['vehicle_list'].append(tmp_json)

					response['vehicle_model_list']=[]
					for o in vehicle_model_data.objects.all():
						tmp_json={}
						tmp_json['id']=o.id
						tmp_json['name']=o.name
						response['vehicle_model_list'].append(tmp_json)

					response['financier_list']=[]
					for o in financier_data.objects.all():
						tmp_json={}
						tmp_json['id']=o.id
						tmp_json['name']=o.name
						response['financier_list'].append(tmp_json)

					response['application_list']=[]
					for o in application_data.objects.all():
						tmp_json={}
						tmp_json['id']=o.id
						tmp_json['name']=o.name
						response['application_list'].append(tmp_json)

					response['location_list']=[]
					for o in location_data.objects.all():
						tmp_json={}
						tmp_json['id']=o.id
						tmp_json['name']=o.name
						response['location_list'].append(tmp_json)
					
				except Exception,e:
					response['success']=False
					response['message']=str(e)
			else:
				response['success']=False
				response['message']="accesstoken not recieved"
		except Exception,e:
			response['success']=False
			response['message']=str(e)
	if request.method=='POST':
		try:
			access_token= request.POST.get("access_token")
			print "access_token :",access_token
			for x,y in request.POST.iteritems():
				print x,y
			if access_token!=None:
				#print "key:",str(KEYS_internal.objects.get(key='jwt').value)
				json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
				try:
					user=user_data.objects.get(id=json_decoded['user_id'])
					user_designation=int(user.designation)

					name=request.POST.get('name')
					mobile=request.POST.get('contact_no')
					address=request.POST.get('address')
					application=request.POST.get('application')
					town=request.POST.get('town')
					district=request.POST.get('district')
					email=request.POST.get('email')
					followup=request.POST.get('followup')
					status=int(request.POST.get('status'))

					date=followup.split('/')
					date=map(int,date)
					followup_date=datetime.datetime(date[2],date[1],date[0])
					
					customer=customer_data.objects.create(name=name,mobile=mobile,address=address,email=email,followup=followup_date,status=status)
					if user_designation==2:
						customer.dse=user
					else:
						dse_id=request.POST.get('user_id')
						dse_user=user_data.objects.get(id=dse_id)
						customer.dse=dse_user
					customer.save()

					vehicle_json_array=json.loads(request.POST.get('vehicle_data_list'))
					for o in vehicle_json_array:
						vehicle_selected_data.objects.create(customer=customer,
							quantity=o['quantity'],
							name=o['name'],
							model=o['model']
							)

				except Exception,e:
					response['success']=False
					response['message']=str(e)
			else:
				response['success']=False
				response['message']="access token not recieved"
		except Exception,e:
			response['success']=False
			response['message']=str(e)
	print response
	return JsonResponse(response)


# def view_customer(request):
# 	response={}
# 	if request.method=='GET':
# 		try:
# 			access_token= request.GET.get("access_token")
# 			print "access_token :",access_token
# 			if access_token!=None:
# 				json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
# 				try:
# 					user=user_data.objects.get(id=json_decoded['user_id'])
# 					user_designation=int(user.designation)
# 		except Exception,e:
# 			response['success']=False
# 			response['message']=str(e)
# 		