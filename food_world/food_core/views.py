from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import User, Snack, Wishlist, Cart, Authenticator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth import hashers
import os
import hmac
import food_world.settings

def generateAuthenticator():
    authenticator = hmac.new(
            key = food_world.settings.SECRET_KEY.encode('utf-8'),
            msg = os.urandom(32),
            digestmod = 'sha256',
        ).hexdigest()
    return authenticator



# Create your views here.

def getCarts(request, pk):
    try:
        cart = Cart.objects.get(pk = pk)
    except:
        return JsonResponse({"status_code": "404"})
    user = cart.user
    total_price = cart.total_price
    num_items = cart.num_items
    return JsonResponse({"status_code": "200", "User": model_to_dict(user), "total_price": total_price, "num_items": num_items})


def getWishlists(request, pk):

    try:
        wishlist= Wishlist.objects.get(pk = pk)
    except:
        return JsonResponse({"status_code": "404"})

    user = wishlist.user
    total_price = wishlist.total_price
    num_items = wishlist.num_items
    return JsonResponse({"status_code": "200", "User": model_to_dict(user), "total_price": total_price, "num_items": num_items} )


def check_user_login(request):
    if request.method == 'GET':
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        try:
            user = User.objects.get(first_name = first_name, last_name = last_name, password = hashers.check_password(password))
            return JsonResponse({"status_code" : '200'})
        except:
            return JsonResponse({'status_code' : '404'})
    return JsonResponse({'status_code' : '500'})

def getUsers(request, pk):
    if request.method == "GET":
        try:
            user = User.objects.get(pk = pk)
        except:
            return JsonResponse({"status_code": "404"})
        first_name = user.first_name
        last_name = user.last_name
        email  = user.email
        phone_number = user.phone_number
        password = user.password

        if hashers.check_password(password) == False:
            return JsonResponse({"status_code": "403"})

        try:
            wishlist = user.wishlist.get()

            wishlist_price = wishlist.total_price
            wishlist_items = wishlist.num_items
        except:
            wishlist = ""
            wishlist_price = ""
            wishlist_items = ""


        try:
            cart = user.cart.get()
            cart_price = cart.get()
            cart_items = cart.num_items
        except:
            cart = ""
            cart_price = ""
            cart_items = ""

            
        return JsonResponse({"status_code": "200", "data" : {'first_name': first_name, "last_name": last_name, "email": email, "phone_number": phone_number, "Wishlist": {"total_price": wishlist_price, "num_items": wishlist_items}, "Cart": {"total_price": cart_price, "num_items": cart_items}}})
    




def getSnacks(request, pk):
    if request.method == "GET":
        try:
            snack = Snack.objects.get(pk = pk)
        except:
            return JsonResponse({"status_code": "404"})
        name = snack.name
        description = snack.description
        price = snack.price
        nutrition_info = snack.nutrition_info
        country = snack.country
        return JsonResponse({"status_code": "200","data" : {"name": name, "description": description, "price": price, "nutrition_info": nutrition_info, "country": country}})
    

def get_all_snacks(request):
    if request.method == "GET":
        all_snack_dict = []
        try:
            snacks = Snack.objects.all()
        except:
            return JsonResponse({"status_code": "404"})

        for snack in snacks:
            name = snack.name
            description = snack.description
            price = snack.price
            nutrition_info = snack.nutrition_info
            country = snack.country


            compiled_snack_data = {"pk" : snack.pk, "name": name, "description": description, "price": price, "nutrition_info": nutrition_info, "country": country}
            all_snack_dict.append(compiled_snack_data)
        return JsonResponse({"status_code": 200,"data" : all_snack_dict})

def get_all_users(request): #Only returns some user info for home screen
    if request.method == "GET":
        all_users_dict = []
        try:
            users = User.objects.all()
        except:
            return JsonResponse({"status_code": "404"})


        for user in users:
            first_name = user.first_name
            last_name = user.last_name
            email  = user.email
            phone_number = user.phone_number
            pk = user.pk
            password = user.password

            compiled_user_data = {'first_name': first_name, "last_name": last_name, "email": email, "phone_number": phone_number, "pk": pk, 'password': password}
            
            all_users_dict.append(compiled_user_data)
            
        return JsonResponse({"status_code": 200,"data" : all_users_dict})


@csrf_exempt
def createUser(request):
    first_name = request.POST.get("first_name", "No first_name Provided")
    last_name = request.POST.get("last_name", "No last_name Provided")
    email  = request.POST.get("email", "No Email Provided")
    password  = request.POST.get("password")
    phone_number = request.POST.get("phone_number", "No phone_number Provided")

    #### Greate Authenticator Model####
    
    try:
        if User.objects.all().filter(email=email).exists() == False:
            new_user = User(first_name = first_name, last_name = last_name, email = email, phone_number = phone_number, password = hashers.make_password(password))
            new_user.save()
            new_auth = Authenticator(user_id = new_user.pk, authenticator = generateAuthenticator())
            new_auth.save()
            new_user.authenticator = new_auth
            return JsonResponse({"status_code": "200", 'id': new_user.id})
        else:
            return JsonResponse({"status_code": "500"})

    except:
        return JsonResponse({"status_code": "500"})

    return JsonResponse({"status_code": "500"})


@csrf_exempt
def createSnack(request):
    name = request.POST.get("name", "No name Provided")
    description  = request.POST.get("description", "No description Provided")
    price = request.POST.get("price", 0.00)
    nutrition_info = request.POST.get("nutrition_info","No nutrition_info Provided")
    country = request.POST.get("country", "No nutrition_info Provided")
    new_snack = Snack(name = name, description = description, price = price, nutrition_info = nutrition_info, country=country)

    try:
        new_snack.save()
        return JsonResponse({"status_code": "200"},)
    except:
        return JsonResponse({"status_code": "500"})


@csrf_exempt
def createCart(request):
    pk = request.POST.get("User", "No user Provided")
    user_item = User.objects.get(pk=pk)
    user = user_item
    total_price = request.POST.get("total_price", 0.00)
    num_items  = request.POST.get("num_items", "No description Provided")
    
    new_cart = Cart(user = user, total_price = total_price, num_items = num_items)
    try:
        new_cart.save()
        return JsonResponse({"status_code": "200"})
    except:
        return JsonResponse({"status_code": "500"})


@csrf_exempt
def createWishlist(request):
    pk = request.POST.get("User", "No user Provided")
    user_item = User.objects.get(pk=pk)
    user = user_item
    total_price = request.POST.get("total_price", 0.00)
    num_items  = request.POST.get("num_items", "No description Provided")
    
    new_wishlist = Wishlist(user = user, total_price = total_price, num_items = num_items)
    try:
        new_wishlist.save()
        return JsonResponse({"status_code": "200"})
    except:
        return JsonResponse({"status_code": "500"})


@csrf_exempt
def destroyUser(request,pk):
    try:
        user = User.objects.get(pk = pk)
        user.delete()
        return JsonResponse({"status_code": "200", })

    except:
        return JsonResponse({"status_code": "500"})

@csrf_exempt
def destroySnack(request,pk):
    try:
        snack = Snack.objects.get(pk = pk)
        snack.delete()
        return JsonResponse({"status_code": "200"})
    except:
        return JsonResponse({"status_code": "500"})

@csrf_exempt
def destroyCart(request,pk):
    try:
        cart = Cart.objects.get(pk = pk)
        cart.delete()
        return JsonResponse({"status_code": "200"})
    except:
        return JsonResponse({"status_code": "500"})

@csrf_exempt
def destroyWishlist(request,pk):
    try:
        wishlist = Wishlist.objects.get(pk = pk)
        wishlist.delete()
        return JsonResponse({"status_code": "200"})
    except:
        return JsonResponse({"status_code": "500"})

@csrf_exempt
def updateUser(request,pk):
    if User.objects.all().filter(pk=pk).exists():
        user = User.objects.get(pk = pk)
        for key, value in request.POST.items():
            setattr(user,key,value)
        user.save()
        return JsonResponse({"status_code": "200", "data" : {'first_name': user.first_name, "last_name": user.last_name, "email": user.email, "phone_number": user.phone_number}})
    else:
        return JsonResponse({"status_code": "500"})

@csrf_exempt
def updateSnack(request,pk):
    if Snack.objects.all().filter(pk=pk).exists():
        snack = Snack.objects.get(pk = pk)
        for key, value in request.POST.items():
             setattr(snack,key,value)
        snack.save()
        name = snack.name
        description = snack.description
        price = snack.price
        nutrition_info = snack.nutrition_info
        country = snack.country
        return JsonResponse({"status_code": "200","data" : {"name": name, "description": description, "price": price, "nutrition_info": nutrition_info, "country": country}})

    else:
        return JsonResponse({"status_code": "500"})

@csrf_exempt
def updateCart(request,pk):
    if Cart.objects.all().filter(pk=pk).exists():
        cart = Cart.objects.get(pk = pk)
        for key, value in request.POST.items():
            setattr(cart,key,value)
        cart.save()
        user = cart.user
        total_price = cart.total_price
        num_items = cart.num_items
        return JsonResponse({"status_code": "200", "User": model_to_dict(user), "total_price": total_price, "num_items": num_items})
    else:
        return JsonResponse({"status_code": "500"})

@csrf_exempt
def updateWishlist(request,pk):
    if Wishlist.objects.all().filter(pk=pk).exists():
        wishlist= Wishlist.objects.get(pk = pk)
        for key, value in request.POST.items():
            setattr(wishlist,key,value)
        wishlist.save()
        
        user = wishlist.user
        total_price = wishlist.total_price
        num_items = wishlist.num_items
        return JsonResponse({"status_code": "200","User": model_to_dict(user), "total_price": total_price, "num_items": num_items})
    else:
        return JsonResponse({"status_code": "500"})

def generate_authenticator(request, pk):
    if User.objects.all().filter(pk=pk).exists():
        user = User.objects.get(pk = pk)
        new_auth = Authenticator(user_id = pk, authenticator = generateAuthenticator())
        new_auth.save()
        user.authenticator = new_auth
        user.save()
        return JsonResponse({"status_code": "200","data" : {'auth' : new_auth.authenticator}})
    else:
        return JsonResponse({"status_code": "500"})



def getAuthenticators(request):
 if request.method == "GET":
        all_auth_dict = []
        try:
            auths = Authenticator.objects.all()
        except:
            return JsonResponse({"status_code": "404"})

        for auth in auths:
            authenticator = auth.authenticator
            user_id = auth.user_id


            compiled_auth_data = {"authenticator": authenticator, "user_id": user_id}
            all_auth_dict.append(compiled_auth_data)
        return JsonResponse({"status_code": 200,"data" : all_auth_dict})

@csrf_exempt
def destroyAuthenticator(request):
    authenticator_token = request.POST.get("authenticator_token")
    if Authenticator.objects.all().filter(authenticator=authenticator_token).exists():
        authenticator_to_delete = Authenticator.objects.all().filter(authenticator=authenticator_token)
        authenticator_to_delete.delete()
        return JsonResponse({"status_code": "200", })  

    return JsonResponse({"status_code": "500"})


