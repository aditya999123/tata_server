from django.shortcuts import render
from keys.models import *
# Create your views here.
from add_user.models import dsm_data,dse_data,user_data
from django.http import JsonResponse
import jwt
def view_users(request):
	response={}
	tmp_array=[]
	try:
		access_token= request.POST.get("access_token")
		print "access_token :",access_token
		if access_token!=None:
			json_decoded=jwt.decode(str(access_token),str(KEYS_internal.objects.get(key='jwt').value), algorithms=['HS256'])
			try:
				user=user_data.objects.get(id=json_decoded['user_id'])
				user_desgination=int(user.designation)
				user_want_type=int(request.GET.get('user_see_type'))
				if(user.active==True):
					
					if(user_designation==0 and user_want_type==1):
						choose_id=int(request.GET.get('choose_id'))
						dealer=dealer_data.objects.get(id=choose_id)
						list=dsm_data.objects.filter(dealer=dealer)

					elif(user_designation==0 and user_want_type==2):
						choose_id=int(request.GET.get('choose_id'))
						if choose_id==-1:
							list= dse_data.objects.all()

						else:
							user_dsm=user_data.objects.get(id=choose_id)
							dsm_user=dsm_data.objects.get(user_id=user_dsm)
							list= dse_data.objects.filter(dsm=dsm_user)

					elif(user_designation==1):
						dsm_user=dsm_data.objects.get(user_id=user)
						list=dse_data.objects.filter(dsm=dsm_user)

					elif(user_designation==0 and user_want_type==3):
						for o in dealer_data.objects.all():
							tmp_json={}
							tmp['id']=o.id
							tmp['name']=o.name
							tmp_array.append(tmp_json)
					else:
						response['success']=False
						response['message']="insufficient access"
					
					if(response['success']==True):
						for o in list:
							tmp_json={}
							tmp['id']=o.user_id.id
							tmp['name']=o.user_id.name
							tmp_array.append(tmp_json)
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
						user_profile=user_data.objects.get(id=user_see_id)
						
						response['name']=user_profile.name
						response['user_name']=user_profile.user_name
						response['mobile']=user_profile.mobile
						response['image']=request.scheme+'://'+request.get_host()+'/media/'+str(user_profile.image)
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
					user=user_data.objects.get(id=json_decoded['user_id'])
					if(user.active==True):
						user.name=request.POST.get('name')
						user.mobile=request.POST.get('mobile')
						user.address=request.POST.get('address')
						user.email=request.POST.get('email')
						image_name=request.FILES.get('profile_image').name
						folder = 'media/users/'+user.user_name+'/'
						try:
							os.mkdir(os.path.join(folder))
						except:
							pass
						tmp_index=0
						saved=False

						while True:
							try:
								fout = open(folder+image_name, 'w')
								file_content = request.FILES.get('profile_image').read()
								fout.write(file_content)
								fout.close()
							except:
								image_name+str(tmp_index)
								tmp_index+=1
						
						user.image=folder+image_name
						user.save()
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
