from django.shortcuts import render
from keys.models import *
# Create your views here.
from add_user.models import *
from customer.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import jwt
import datetime
report_flag=False
def view_users(request):
	response={}
	tmp_array=[]
	try:
		access_token= request.GET.get("access_token")
		print "access_token :",access_token
		for x,y in request.GET.iteritems():
			print x,y
		if access_token!=None:
			json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
			try:
				user=user_data.objects.get(id=json_decoded['user_id'])
				user_designation=int(user.designation)
				user_want_type=int(request.GET.get('user_see_type'))
				#try:
				to_date=request.GET.get('to_date')
				date=to_date.split('/')
				date=map(int,date)
				to_date=datetime.datetime(date[2],date[1],date[0])
				
				from_date=request.GET.get('from_date')
				date=from_date.split('/')
				date=map(int,date)
				from_date=datetime.datetime(date[2],date[1],date[0])
				# except Exception,e:
				# 	print e
				# 	from_date=datetime.datetime.now().date()
				# 	to_date=datetime.datetime.now()+datetime.timedelta(1)
				# 	to_date=to_date.date()
				if(user.active==True):
					print"@20"
					print "user_designation",user_designation
					print "user_want_type",user_want_type
					response['success']=True
					if(user_designation==0 and user_want_type==1):
						choose_id=int(request.GET.get('choose_id'))
						print "choose_id",choose_id
						if choose_id==-1:
							list=dsm_data.objects.all()
						else:
							dealer=dealer_data.objects.get(id=choose_id)
							list=dsm_data.objects.filter(dealer=dealer)

					elif(user_designation==0 and user_want_type==2):
						choose_id=int(request.GET.get('choose_id'))
						if choose_id==-1:
							list= dse_data.objects.all()
						else:
							#user_dsm=user_data.objects.get(id=choose_id)
							dsm_user=dsm_data.objects.get(id=choose_id)
							list= dse_data.objects.filter(dsm=dsm_user)

					elif(user_designation==1 and user_want_type==2):
						dsm_user=dsm_data.objects.get(user_id=user)
						list=dse_data.objects.filter(dsm=dsm_user)

					elif(user_designation==0 and user_want_type==3):
						for o in dealer_data.objects.all():
							tmp_json={}
							tmp_json['id']=o.id
							tmp_json['name']=o.name
							tmp_array.append(tmp_json)

					elif(user_want_type==4):
						choose_id=int(request.GET.get('choose_id'))
						print "choose_id",choose_id
						#user_dse=user_data.objects.get(id=choose_id)
						if choose_id==-1:
							#dse_user=dse_data.objects.get(id=choose_id)
							#print dse_user.user_id.name
							for o in customer_data.objects.all():#filter(dse=dse_user):
								tmp_json={}
								tmp_json['id']=o.id
								tmp_json['name']=o.name
								tmp_array.append(tmp_json)
						else:
							dse_user=dse_data.objects.get(id=choose_id)
							print dse_user.user_id.name
							for o in customer_data.objects.filter(dse=dse_user):
								tmp_json={}
								tmp_json['id']=o.id
								tmp_json['name']=o.name
								tmp_array.append(tmp_json)
					else:
						response['success']=False
						response['message']="insufficient access"
					try:

						print"here@78"
						if(response['success']==True):
							for o in list:
								try:
									print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@82"
									tmp_json={}
									tmp_json['id']=o.id
									tmp_json['name']=o.user_id.name
									tmp_json['user_id']=o.user_id.id
									if user_want_type==2:			
										tmp_json['daily_target']=o.dsm.target_daily_dse
										print "datexxx",from_date
										print "datexxx",to_date
										customer_list=customer_data.objects.filter(dse=o,created__range=[from_date,to_date])
										for fol in followup_data.objects.filter(created__range=[from_date,to_date],customer__dse=o):
											if fol.customer not in customer_list:
												customer_list.append(fol.customer)
										tmp_json['customer_met']=customer_list.count()
										tmp_json['pending']=customer_list.filter(status=0).count()
										tmp_json['sold']=customer_list.filter(status=1).count()
										tmp_json['lost']=customer_list.filter(status=2).count()
										green=0
										red=1
										tmp_json['colour_flag']=green
										if from_date==datetime.datetime.now().date():
											if report_flag==True:
												if o.tagret_achieved==False:
													if(o.customer_reached_today<o.daily_target):
														tmp_json['colour_flag']=red
													else:
														for cust in customer_data.objects.filter(dse=o):
															if(cust.followup<datetime.datetime.now().date()):
																tmp_json['colour_flag']=red
																break
									if user_want_type==1:
										a=0
										b=0
										c=0
										d=0
										print o
										for ds in dse_data.objects.filter(dsm=o):
											tmp_json['daily_target']=o.target_daily_dse
											print ds
											customer_list=customer_data.objects.filter(dse=ds,created__range=[from_date,to_date])
											for fol in followup_data.objects.filter(created__range=[from_date,to_date],customer__dse=ds):
												print "xyz"
												if fol.customer not in customer_list:
													customer_list.append(fol.customer)
											a=a+customer_list.count()
											b=b+customer_list.filter(status=0).count()
											c=c+customer_list.filter(status=1).count()
											d=d+customer_list.filter(status=2).count()

										tmp_json['customer_met']=a
										tmp_json['pending']=b
										tmp_json['sold']=c
										tmp_json['lost']=d

									tmp_array.append(tmp_json)
								except Exception,e:
									response['success']=False
									response['message']=str(e)
					except:
						pass
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
	response['user_list']=tmp_array

	print response
	return JsonResponse(response)

user_type_deg={0:'TSM',1:'DSM',2:'DSE'}
@csrf_exempt
def view_profile(request):
	response={}
	if request.method=='GET':
		try:
			access_token= request.GET.get("access_token")
			print "access_token :",access_token
			if access_token!=None:
				json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
				try:
					user=user_data.objects.get(id=json_decoded['user_id'])
					if(user.active==True):
						user_see_id=request.GET.get('user_id')
						print 'user_see_id',user_see_id
						user_profile=user_data.objects.get(id=int(user_see_id))
						print "arpit_chu"
						response['name']=user_profile.name
						response['user_name']=user_profile.user_name
						response['mobile']=user_profile.mobile
						response['image']=request.scheme+'://'+request.get_host()+str(user_profile.image)
						response['address']=user_profile.address
						response['designation']=user_type_deg[int(user_profile.designation)]
						response['email']=user_profile.email
						response['success']=True
						response['message']="Profile"
						#response['profile_data']=response
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

	if request.method=='POST':
		try:
			access_token= request.POST.get("access_token")
			print "access_token :",access_token
			if access_token!=None:
				json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
				try:
					print "addd",request.POST.get('user_id')
					for x,y in request.POST.iteritems():
						print x,y
					user=user_data.objects.get(id=int(request.POST.get('user_id')))
					if(user.active==True):
						user.name=request.POST.get('name')
						user.mobile=request.POST.get('mobile')
						user.address=request.POST.get('address')
						user.email=request.POST.get('email')
						#image_name=request.FILES.get('profile_image').name
						#folder = 'media/users/'+user.user_name+'/'
						#try:
						#	os.mkdir(os.path.join(folder))
						#except:
						#	pass
						#tmp_index=0
						#saved=False

						#while True:
							# try:
							# 	fout = open(folder+image_name, 'w')
							# 	file_content = request.FILES.get('profile_image').read()
							# 	fout.write(file_content)
							# 	fout.close()
							# except:
							# 	image_name+str(tmp_index)
							# 	tmp_index+=1
						
						#user.image=folder+image_name
						user.save()
						response['success']=True
						response['message']="updated"
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
	
	print response
	return JsonResponse(response)
