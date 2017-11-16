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

	auth = request.COOKIES.get('auth')

	print("indexed")

	if not auth:
		return render(request, 'index.html', {"context" : context, 'status': 'Login', 'url': '/login/'} )
	else:


		return render(request, 'index.html', {"context" : context, 'status': 'Logout' , 'url': '/logout/'} )

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

	auth = request.COOKIES.get('auth')

	if auth:
		response = HttpResponseRedirect(reverse('home'))
		return response


	if request.method == 'GET':	
		return render(request, 'login.html', {"context": login_form})

	if not login_form.is_valid():
		return render(request,'login.html', {"context": login_form})


	email = login_form.cleaned_data['email']
	password = login_form.cleaned_data['password']

	url = 'http://exp-api:8000/api/v1/login/'
	data = {'email': email,  'password': password}
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

@csrf_exempt
def logout(request):
	response = HttpResponseRedirect(reverse('home'))
	cookie = request.COOKIES.get('auth')
	response.delete_cookie('auth')
	
	url = 'http://exp-api:8000/api/v1/logout/'
	data = {'authenticator_token' : cookie}
	data = bytes( urllib.parse.urlencode( data ).encode() )
	handler = urllib.request.urlopen(url, data);
	return response


@csrf_exempt
def register(request):
	register_form = forms.RegisterForm(request.POST)
	if request.method == 'GET':	
		return render(request, 'register.html', {"context": register_form})


	if not register_form.is_valid():
		return render(request,'register.html', {"context": register_form, "error" : "Error! Invalid form"})

	first_name = register_form.cleaned_data['first_name']
	last_name = register_form.cleaned_data['last_name']
	password = register_form.cleaned_data['password']
	email = register_form.cleaned_data['email']
	phone_number = register_form.cleaned_data['phone_number']


	url = 'http://exp-api:8000/api/v1/register/'
	data = {'first_name' : first_name, 'last_name': last_name, 'password': password, 'email': email, 'phone_number': phone_number}
	data = bytes( urllib.parse.urlencode( data ).encode() )
	handler = urllib.request.urlopen(url, data);
	

	post_feedback = handler.read().decode('utf-8')
	resp = json.loads(post_feedback)
	response = resp['status_code']


	if response != '200':
		# Couldn't log them in, send them back to login page with error
			return render(request,'register.html', {"context": register_form, "error" : "Error! Email already exists!"})
	
	response = HttpResponseRedirect(reverse('login'))
	return response

@csrf_exempt
def create_snack(request):
	create_Snack_form = forms.CreateSnackForm()
	auth = request.COOKIES.get('auth')

	if not auth:
		return HttpResponseRedirect(reverse("login"))
	if request.method == 'GET':
		return render(request, 'createSnack.html', {"context": create_Snack_form})

	url = 'http://exp-api:8000/api/v1/create_snack/'

	name = request.POST.get("name", "No name Provided")
	description  = request.POST.get("description", "No description Provided")
	price = request.POST.get("price", 0.00)
	nutrition_info = request.POST.get("nutrition_info","No nutrition_info Provided")
	country = request.POST.get("country", "No nutrition_info Provided")
	data = {'name' : name, 'description': description, 'price': price, 'nutrition_info': nutrition_info, 'country':country, 'auth': auth}
	data = bytes( urllib.parse.urlencode( data ).encode() )
	handler = urllib.request.urlopen(url, data);


	post_feedback = handler.read().decode('utf-8')
	resp = json.loads(post_feedback)
	response = resp['status_code']

	if response != '200':
		return render(request, 'createSnack.html', {"context": create_Snack_form, 'return_status': "Whoops! There has Been An Error Processing Your Request"})

	return render(request, 'createSnack.html', {"context": create_Snack_form, 'return_status': "Success! Your Snack Has Been Created!"})


@csrf_exempt
def search(request):
	url = 'http://exp-api:8000/api/v1/search/'
	search_input = request.POST.get("search", "")
	data = {'search_input' : search_input}
	data = bytes( urllib.parse.urlencode( data ).encode() )
	handler = urllib.request.urlopen(url, data);
	
	post_feedback = handler.read().decode('utf-8')
	resp = json.loads(post_feedback)
	response = resp['status_code']

	if response != '200':
		return HttpResponseRedirect(reverse('home'))
	snack_dict = []
	search_results = resp['data']
	for result in search_results:
		snack = result["_source"]
		snack_dict.append(snack)
	return render(request, 'sorted.html', {"context": snack_dict})
