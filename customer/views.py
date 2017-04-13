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
def fetch_vehicle_selected(response,customer):
	response['vehicle_selected_data_list']=[]
	for o in vehicle_selected_data.objects.filter(customer=customer):
		tmp_json={}
		tmp_json['id']=o.id
		tmp_json['quantity']=o.quantity
		tmp_json['vehicle']=o.name
		tmp_json['model']=o.model
		response['vehicle_selected_data_list'].append(tmp_json)
	return response


def fetch_options(response,user,user_designation=0):
	global report_flag

	response['user_list']=[]
	if user_designation==0:
		for o in dse_data.objects.all():
			tmp_json={}
			tmp_json['name']=o.user_id.name+' - '+o.dsm.user_id.name
			tmp_json['id']=o.id
			response['user_list'].append(tmp_json)
	print"@36"
	if user_designation==1:
		dsm_user=dsm_data.objects.get(user_id=user)
		for o in dse_data.objects.filter(dsm=dsm_user):
			tmp_json={}
			tmp_json['name']=o.user_id.name
			tmp_json['id']=o.id
			response['user_list'].append(tmp_json)
	response['district_list']=[]
	print"@44"
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

	return response
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
					response['success']=True
					response['message']="success"
					user=user_data.objects.get(id=json_decoded['user_id'])
					user_designation=int(user.designation)
					response = fetch_options(response,user,user_designation)
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

					name=request.POST.get('customer_name')
					mobile=request.POST.get('contact_no')
					address=request.POST.get('address')
					application=request.POST.get('application')
					town=request.POST.get('town')
					district=request.POST.get('district')
					email=request.POST.get('email')
					tehsil=request.POST.get('tehsil')
					
					status=int(request.POST.get('status'))
					financier=request.POST.get('financier')
					location=request.POST.get('location')
					
					followup=request.POST.get('followup')
					date=followup.split('/')
					date=map(int,date)
					followup_date=datetime.datetime(date[2],date[1],date[0])
					
					customer=customer_data.objects.create(name=name,
						mobile=mobile,
						address=address,
						email=email,
						followup=followup_date,
						status=status,
						application=application,
						town=town,
						district=district,
						tehsil=tehsil,
						financier=financier,
						location=location
						)
					print "@162"
					if user_designation==2:
						customer.dse=user
						user.customer_reached_today=user.customer_reached_today+1
						user.save()
					else:
						dse_id=request.POST.get('user_id')
						dse_user=dse_data.objects.get(id=dse_id)
						customer.dse=dse_user
						dse_user.customer_reached_today=dse_user.customer_reached_today+1
						dse_user.save()
					customer.save()

					vehicle_json=json.loads(request.POST.get('vehicle_data_list'))
					vehicle_json_array=vehicle_json['item']
					for o in vehicle_json_array:
						vehicle_selected_data.objects.create(customer=customer,
							quantity=o['quantity'],
							name=o['vehicle'],
							model=o['model']
							)
					response['success']=True
					response['message']="success"

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

@csrf_exempt
def edit_customer(request):
	response={}
	if request.method=='GET':
		try:
			access_token= request.GET.get("access_token")
			print "access_token :",access_token
			if access_token!=None:
				response['success']=True
				response['message']="success"
				json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
				try:
					user=user_data.objects.get(id=json_decoded['user_id'])
					user_designation=int(user.designation)

					customer_id=request.GET.get('choose_id')
					customer=customer_data.objects.get(id=customer_id)
					response=fetch_options(response,user,user_designation)

					response['customer_name']=customer.name
					response['contact_no']=customer.mobile
					response['address']=customer.address
					response['email']=customer.email
					response['followup']=str(customer.followup.strftime("%d/%m/%y"))
					response['status']=customer.status
					response['application']=customer.application
					response['town']=customer.town
					response['district']=customer.district
					response['tehsil']=customer.tehsil
					response['financier']=customer.financier
					response['location']=customer.location
					response=fetch_vehicle_selected(response,customer)

				except Exception,e:
					response['success']=False
					response['message']=str(e)
		except Exception,e:
			response['success']=False
			response['message']=str(e)

	if request.method=='POST':
		access_token= request.POST.get("access_token")
		print "access_token :",access_token
		if access_token!=None:
			response['success']=True
			response['message']="success"
			json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
			try:
				user=user_data.objects.get(id=json_decoded['user_id'])
				user_designation=int(user.designation)


				response['success']=True
				response['message']="followup entry created"

				name=request.POST.get('customer_name')
				mobile=request.POST.get('contact_no')
				address=request.POST.get('address')
				application=request.POST.get('application')
				town=request.POST.get('town')
				district=request.POST.get('district')
				email=request.POST.get('email')
				tehsil=request.POST.get('tehsil')
				followup=request.POST.get('followup')
				status=int(request.POST.get('status'))
				financier=request.POST.get('financier')
				location=request.POST.get('location')
				customer_id=request.POST.get('choose_id')
				vehicle_json=json.loads(request.POST.get('vehicle_data_list'))
				customer=customer_data.objects.get(id=customer_id)
				
				vehicle_json_array=vehicle_json['item']
				for o in vehicle_json_array:
					v_quantity=o['quantity']
					v_name=o['vehicle']
					v_model=o['model']
					v_id=o['id']
					vehicle_selected=vehicle_selected_data.objects.get(id=v_id)
					vehicle_selected.name=v_name
					vehicle_selected.model=v_model
					vehicle_selected.quantity=v_quantity
					vehicle_selected.save()	
					
				customer.name=name
				customer.mobile=mobile
				customer.address=address
				customer.application=application
				customer.town=town
				customer.district=district
				customer.email=email
				customer.tehsil=tehsil
				
				date=followup.split('/')
				date=map(int,date)
				followup_date=datetime.datetime(date[2],date[1],date[0])

				customer.followup=followup_date
				customer.status=status
				customer.location=location
				if user_designation<=1:
					dse_id=request.POST.get('user_id')
					dse_user=dse_data.objects.get(id=dse_id)
					customer.dse=dse_user

				##################################3if followup to be counted in target
				# if(customer.modified.date()<datetime.datetime.now().date()):
				# 	customer.dse.customer_reached_today=customer.dse.customer_reached_today+1
				# 	customer.dse.save()

				customer.save()
				response=fetch_vehicle_selected(response,customer)
				followup_data.objects.create(customer=customer,followupby=user.name)

			except Exception,e:
				response['success']=False
				response['message']=str(e)
		else:
			response['success']=False
			response['message']="no access token recieved"
	print response
	return JsonResponse(response)
def view_customer(request):
	response={}
	if request.method=='GET':
		try:
			access_token= request.GET.get("access_token")
			print "access_token :",access_token
			if access_token!=None:
				response['success']=True
				response['message']="success"
				json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
				try:
					print"@288"
					user=user_data.objects.get(id=json_decoded['user_id'])
					user_designation=int(user.designation)
					print"@290"
					customer_id=request.GET.get('choose_id')
					customer=customer_data.objects.get(id=customer_id)
					#response=fetch_options(response)

					response['customer_name']=customer.name
					response['contact_no']=customer.mobile
					response['address']=customer.address
					response['email']=customer.email
					response['followup']=str(customer.followup.strftime("%d/%m/%y"))
					response['status']=customer.status
					response['application']=customer.application
					response['town']=customer.town
					response['district']=customer.district
					response['tehsil']=customer.tehsil
					response['financier']=customer.financier
					response['location']=customer.location

					response=fetch_vehicle_selected(response,customer)

				except Exception,e:
					response['success']=False
					response['message']=str(e)
		except Exception,e:
			response['success']=False
			response['message']=str(e)
	else:
		response['success']=False
		response['message']="not get"

	print response
	return JsonResponse(response)


def followup_list(request):
	response={}
	if request.method=='GET':
		try:
			access_token= request.GET.get("access_token")
			print "access_token :",access_token
			if access_token!=None:
				response['success']=True
				response['message']="success"
				json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
				try:
					customer_id=request.GET.get('customer_id')
					customer=customer_data.objects.get(id=customer_id)

					response['followup_list']=[]
					for o in followup_data.objects.filter(customer=customer):
						tmp_json={}
						tmp_json['id']=o.id
						tmp_json['name']=o.followupby
						tmp_json['date']=str(o.created)[:19]
						#time adjustment
						response['followup_list'].append(tmp_json)
				except Exception,e:
					response['success']=False
					response['message']=str(e)
			else:
				response['success']=False
				response['message']="acccess token no recieved"
		except Exception,e:
			response['success']=False
			response['message']=str(e)
	else:
		response['success']=False
		response['message']="post method"

	print response
	return JsonResponse(response)