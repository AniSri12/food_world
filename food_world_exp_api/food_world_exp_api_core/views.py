from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import hashers
from kafka import KafkaProducer
from elasticsearch import Elasticsearch

# Create your views here.


def index(request):
	print ("About to perform the GET request...")
	req_snacks = urllib.request.Request('http://models-api:8000/api/v1/snacks/')
	req_users = urllib.request.Request('http://models-api:8000/api/v1/users/')
	resp_snacks = urllib.request.urlopen(req_snacks).read().decode('utf-8')
	resp_users = urllib.request.urlopen(req_users).read().decode('utf-8')
	json_snacks = json.loads(resp_snacks)
	json_users = json.loads(resp_users)
	return_data = {"status_code:": 200, "data": {"users": json_users, "snacks": json_snacks}}

	return JsonResponse(return_data)

def sort(request):
	print ("About to perform the GET request...")
	req_snacks = urllib.request.Request('http://models-api:8000/api/v1/snacks/')
	resp_snacks = urllib.request.urlopen(req_snacks).read().decode('utf-8')
	json_snacks = json.loads(resp_snacks)
	newlist = sorted(json_snacks['data'], key=lambda k: k['country']) 
	return_data = {"status_code:": 200, "data": newlist}

	return JsonResponse(return_data)


def details(request,pk):
	req_snack = urllib.request.Request('http://models-api:8000/api/v1/snacks/' + pk)
	resp_snack = urllib.request.urlopen(req_snack).read().decode('utf-8')
	json_snack = json.loads(resp_snack)
	return_data = {"status_code:": 200, "data": {"snack": json_snack}}
	return JsonResponse(return_data)


@csrf_exempt
def validate_user(request):
	req_users = urllib.request.Request('http://models-api:8000/api/v1/users/')
	resp_users = urllib.request.urlopen(req_users).read().decode('utf-8')
	json_users = json.loads(resp_users)['data']


	email = request.POST['email']
	password = request.POST['password']

	for user in json_users:
		if user['email'] == email and hashers.check_password(password, user['password']):			
			authenticator = urllib.request.Request('http://models-api:8000/api/v1/create_auth/' + str(user['pk']) )
			resp_auth = urllib.request.urlopen(authenticator).read().decode('utf-8')
			json_auth = json.loads(resp_auth)

			if json_auth ['status_code'] == '200':
				return JsonResponse({'status_code': '200', 'auth' : json_auth ['data']['auth'], 'pk': user['pk']})
	
	return JsonResponse({'status_code': '404'})



@csrf_exempt
def register(request):
	first_name = request.POST.get("first_name")
	last_name = request.POST.get("last_name")
	email = request.POST.get("email")
	phone_number = request.POST.get("phone_number")
	password = request.POST.get("password")

	url = 'http://models-api:8000/api/v1/users/create'
	data = {'first_name' : first_name, 'last_name': last_name, 'password': password, 'email': email, 'phone_number': phone_number}
	data = bytes( urllib.parse.urlencode( data ).encode() )
	handler = urllib.request.urlopen(url, data);
	

	post_feedback = handler.read().decode('utf-8')
	resp = json.loads(post_feedback)
	return JsonResponse(resp)

@csrf_exempt
def create_snack(request):
	url = 'http://models-api:8000/api/v1/snacks/create'

	req_auths = urllib.request.Request('http://models-api:8000/api/v1/auths/')
	resp_auths = urllib.request.urlopen(req_auths).read().decode('utf-8')
	json_auths = json.loads(resp_auths)['data']

	name = request.POST.get("name", "No name Provided")
	description  = request.POST.get("description", "No description Provided")
	price = request.POST.get("price", 0.00)
	nutrition_info = request.POST.get("nutrition_info","No nutrition_info Provided")
	country = request.POST.get("country", "No nutrition_info Provided")
	auth = request.POST.get("auth", "No Auth Provided")
	for authenticator in json_auths:
		if authenticator["authenticator"] == auth:
			data_vals = {'name' : name, 'description': description, 'price': price, 'nutrition_info': nutrition_info, 'country' : country}
			
			data = bytes( urllib.parse.urlencode( data_vals ).encode() )
			handler = urllib.request.urlopen(url, data);
			

			post_feedback = handler.read().decode('utf-8')
			resp = json.loads(post_feedback)

			resp['Data'] = data_vals

			##### Kafka section: ######
			producer = KafkaProducer(bootstrap_servers='kafka:9092')
			send_new_listing = resp
			producer.send('new-snack', json.dumps(send_new_listing).encode('utf-8'))
			#### End of Kafka section ####

			return JsonResponse(resp)

	return JsonResponse({'status_code': '403'})

@csrf_exempt
def search(request):
	es = Elasticsearch(['es'])
	if request.method == 'POST':
		query = request.POST.get('search_input')
		query_results = es.search(index='listing_index', body={'query': {'query_string': {'query': query}}, 'size': 10})

		results = []
		for snack in query_results['hits']['hits']:
			results.append(snack)

		return JsonResponse({'status_code': '200', 'data': results})

	return JsonResponse({'status_code': '500'})


@csrf_exempt
def logout(request):
	url = 'http://models-api:8000/api/v1/destroy_auth/'
	cookie = request.POST.get('authenticator_token')
	data = {'authenticator_token' : cookie}
	data = bytes( urllib.parse.urlencode( data ).encode() )
	handler = urllib.request.urlopen(url, data);

	return JsonResponse({'status_code': '200'})



