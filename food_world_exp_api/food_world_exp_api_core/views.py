from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
	url = 'http://models-api:8000/api/v1/login/'
	first_name = request.POST['first_name']
	last_name = request.POST['last_name']
	password = request.POST['password']

	data = {'first_name' : first_name, 'last_name': last_name, 'password': password}
	resp = urllib.request.Request(url, data= data)

	if resp['status_code'] == "200":
		return 'ok'
	else:
		return 'invalid'