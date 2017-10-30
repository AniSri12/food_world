from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
from . import forms
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

@csrf_exempt
def index(request):
	req_home= urllib.request.Request('http://exp-api:8000/api/v1/')
	resp_home= urllib.request.urlopen(req_home).read().decode('utf-8')
	resp = json.loads(resp_home)
	context = resp["data"]
	return render(request, 'index.html', {"context" : context} )


def details(request,pk):
	req_details= urllib.request.Request('http://exp-api:8000/api/v1/snacks/' + pk)
	resp_details= urllib.request.urlopen(req_details).read().decode('utf-8')
	resp = json.loads(resp_details)
	context = resp["data"]
	return render(request, 'details.html', {"context" : context })

def sort(request):
	req_details= urllib.request.Request('http://exp-api:8000/api/v1/sorted/')
	resp_details= urllib.request.urlopen(req_details).read().decode('utf-8')
	resp = json.loads(resp_details)
	context = resp["data"]
	return render(request, 'sorted.html', {"context" : context })

@csrf_exempt
def login(request):
	login_form = forms.LoginForm(request.POST)
	next = request.GET.get('next') or reverse('home')
	if request.method == 'GET':	
		return render(request, 'login.html', {"context": login_form})

	if not login_form.is_valid():
		return render(request,'login.html', {"context": login_form})


	first_name = login_form.cleaned_data['first_name']
	last_name = login_form.cleaned_data['last_name']
	password = login_form.cleaned_data['password']

	url = 'http://exp-api:8000/api/v1/login/'
	data = {'first_name' : first_name, 'last_name': last_name, 'password': password}
	data = bytes( urllib.parse.urlencode( data ).encode() )
	handler = urllib.request.urlopen(url, data);
	

	post_feedback = handler.read().decode('utf-8')
	resp = json.loads(post_feedback)
	response = resp['status_code']
	if response != '200':
	# Couldn't log them in, send them back to login page with error
		return render(request,'login.html', {"context": login_form , "error" : "Error! Invalid Login"})

	# Set their login cookie and redirect to back to wherever they came from
	authenticator = resp['auth']


	response = HttpResponseRedirect(reverse('home'))



	response.set_cookie("auth", authenticator)

	return response



def register(request):
	register_form = forms.RegisterForm()
	return render(request, 'register.html', {"context": register_form})

@csrf_exempt
def create_snack(request):
	create_Snack_form = forms.CreateSnackForm()
	auth = request.COOKIES.get('auth')
	if not auth:
		return HttpResponseRedirect(reverse("login"))
	if request.method == 'GET':
		return render(request, 'createSnack.html', {"context": create_Snack_form})

    # Otherwise, create a new form instance with our POST data



	return render(request, 'createSnack.html', {"context": create_Snack_form})





