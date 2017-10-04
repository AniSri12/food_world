from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse


def index(request):
	req_home= urllib.request.Request('localhost:8002/api/v1/')
	# resp_home= urllib.request.urlopen(req_home).read().decode('utf-8')
	# resp = json.loads(resp_home)

	return render(request, 'index.html')