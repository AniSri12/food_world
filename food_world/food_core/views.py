from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import User, Snack, Wishlist, Cart
from django.views.decorators.csrf import csrf_exempt




# Create your views here.

def getCarts(request, pk):
    try:
        cart = Cart.objects.get(pk = pk)
    except:
        return JsonResponse({"status_code": "404"})
        user = cart.user
        total_price = cart.total_price
        num_items = cart.num_items
        return JsonResponse({"status_code": "200", "User": user, "total_price": total_price, "num_items": num_items})


def getWishlists(request, pk):

    try:
        wishlist= Wishlist.objects.get(pk = pk)
    except:
        return JsonResponse({"status_code": "404"})

    user = wishlist.user
    total_price = wishlist.total_price
    num_items = wishlist.num_items
    return JsonResponse({"status_code": "200","User": user, "total_price": total_price, "num_items": num_items})



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

            compiled_user_data = {'first_name': first_name, "last_name": last_name, "email": email, "phone_number": phone_number, "pk": pk}
            
            all_users_dict.append(compiled_user_data)
            
        return JsonResponse({"status_code": 200,"data" : all_users_dict})


@csrf_exempt
def createUser(request):
    first_name = request.POST.get("first_name", "No first_name Provided")
    last_name = request.POST.get("last_name", "No last_name Provided")
    email  = request.POST.get("Email", "No Email Provided")
    phone_number = request.POST.get("phone_number", "No phone_number Provided")
    new_user = User(first_name = first_name, last_name = last_name, email = email, phone_number = phone_number)
    
    try:
        new_user.save()
        return JsonResponse({"status_code": "200"})
    except:
        return JsonResponse({"status_code": "500"})

@csrf_exempt
def createSnack(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    name = body.get("name", "No name Provided")
    description  = body.get("description", "No description Provided")
    price = body.get("price", 0.00)
    nutrition_info = body.get("nutrition_info","No nutrition_info Provided")
    country = body.get("country", "No nutrition_info Provided")
    new_snack = Snack(name = name, description = description, price = price, nutrition_info = nutrition_info)

    try:
        new_snack.save()
        return JsonResponse({"status_code": "200"})
    except:
        return JsonResponse({"status_code": "500"})


@csrf_exempt
def createCart(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user = body.get("User", "No user Provided")
    total_price = body.get("total_price", 0.00)
    num_items  = body.get("Num Items", "No description Provided")
    
    new_cart = Cart(user = user, total_price = total_price, num_items = num_items)
    try:
        new_cart.save()
        return JsonResponse({"status_code": "200", "nameTest": request.POST})
    except:
        return JsonResponse({"status_code": "500"})


@csrf_exempt
def createWishlist(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user = body.get("User", "No user Provided")
    total_price = body.get("total_price", 0.00)
    num_items  = body.get("Num Items", "No description Provided")
    
    new_wishlist = Wishlist(user = user, total_price = total_price, num_items = num_items)
    try:
        new_wishlist.save()
        return JsonResponse({"status_code": "200", "nameTest": request.POST})
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
    except:
        return JsonResponse({"status_code": "500"})

@csrf_exempt
def destroyCart(request,pk):
    try:
        cart = Cart.objects.get(pk = pk)
        cart.delete()
    except:
        return JsonResponse({"status_code": "500"})

@csrf_exempt
def destroyWishlist(request,pk):
    try:
        wishlist = Wishlist.objects.get(pk = pk)
        wishlist.delete()
    except:
        return JsonResponse({"status_code": "500"})

@csrf_exempt
def updateUser(request,pk):
    try:
        user, created = User.objects.update_or_create(
        pk=pk, defaults=request.POST)
        return JsonResponse({"status_code": "200", "data" : {'first_name': user.first_name, "last_name": user.last_name, "email": user.email, "phone_number": user.phone_number}})
    except:
        return JsonResponse({"status_code": "500"})

@csrf_exempt
def updateSnack(request,pk):
    try:
        snack = Snack.objects.get(pk = pk)
        for key, value in request.POST:
            snack.key = value
        snack.save()
        return JsonResponse({"status_code": "200","data" : {"name": name, "description": description, "price": price, "nutrition_info": nutrition_info}})
    except:
        return JsonResponse({"status_code": "500"})
    # try:
    #     snack, created = Snack.objects.update_or_create(
    #     pk=pk, defaults=request.POST)
    #     return JsonResponse({"status_code": "200","data" : {"name": name, "description": description, "price": price, "nutrition_info": nutrition_info}})
    # except:
    #     return JsonResponse({"status_code": "500"})

@csrf_exempt
def updateCart(request,pk):
    try:
        cart, created = Cart.objects.update_or_create(
        pk=pk, defaults=request.POST)
        return JsonResponse({"status_code": "200", "User": user, "total_price": total_price, "num_items": num_items})
    except:
        return JsonResponse({"status_code": "500"})

@csrf_exempt
def updateWishlist(request,pk):
    try:
        wishlist, created = Wishlist.objects.update_or_create(
        pk=pk, defaults=request.POST)
        return JsonResponse({"status_code": "200","User": user, "total_price": total_price, "num_items": num_items})
    except:
        return JsonResponse({"status_code": "500"})

