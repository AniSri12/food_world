from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse


def index(request):
	req_home= urllib.request.Request('http://exp-api:8000/api/v1/')
	resp_home= urllib.request.urlopen(req_home).read().decode('utf-8')
	resp = json.loads(resp_home)
	context = resp["Data"]
	return render(request, 'index.html', {"Context" : context })


def details(request,pk):
	req_details= urllib.request.Request('http://exp-api:8000/api/v1/snacks/' + pk)
	resp_details= urllib.request.urlopen(req_details).read().decode('utf-8')
	resp = json.loads(resp_details)
	context = resp["Data"]
	return render(request, 'details.html', {"Context" : context })