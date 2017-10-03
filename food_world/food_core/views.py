from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import User, Snack, Wishlist, Cart
from django.views.decorators.csrf import csrf_exempt




# Create your views here.

# def getCarts(request, pk):
#   try:
#       cart = Cart.objects.get(pk = pk)
#   except:
#       return JsonResponse({"Status Code": "404"})
#   user = cart.user
#   total_price = cart.total_price
#   num_items = cart.num_items
#   return JsonResponse({"Status Code": "200", "User": user, "Total Price": total_price, "Number of Items": num_items})


# def getWishlist(request, pk):

#   try:
#       wishlist= Wishlist.objects.get(pk = pk)
#   except:
#       return JsonResponse({"Status Code": "404"})

#   user = wishlist.user
#   total_price = wishlist.total_price
#   num_items = wishlist.num_items
#   return JsonResponse({"Status Code": "200","User": user, "Total Price": total_price, "Number of Items": num_items})



def getUsers(request, pk):
    try:
        user = User.objects.get(pk = pk)
    except:
        return JsonResponse({"Status Code": "404"})
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

        
    return JsonResponse({"Status Code": "200", 'First Name': first_name, "Last Name": last_name, "email": email, "Phone Number": phone_number, "Wishlist": {"Total Price": wishlist_price, "Number of Items": wishlist_items}, "Cart": {"Total Price": cart_price, "Number of Items": cart_items}})



def getSnacks(request, pk):
    try:
        snack = Snack.objects.get(pk = pk)
    except:
        return JsonResponse({"Status Code": "404"})
    name = snack.name
    description = snack.description
    price = snack.price
    nutrition_info = snack.nutrition_info
    return JsonResponse({"Status Code": "200","Name": name, "Description": description, "Price": price, "Nutrition Info": nutrition_info})






@csrf_exempt
def createUser(request):
    first_name = request.POST.get("First Name", "No First Name Provided")
    last_name = request.POST.get("Last Name", "No Last Name Provided")
    email  = request.POST.get("Email", "No Email Provided")
    phone_number = request.POST.get("Phone Number", "No Phone Number Provided")
    new_user = User(first_name = first_name, last_name = last_name, email = email, phone_number = phone_number)
    
    try:
        new_user.save()
        return JsonResponse({"Status Code": "200"})
    except:
        return JsonResponse({"Status Code": "500"})

@csrf_exempt
def createSnack(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    name = body.get("Name", "No Name Provided")
    description  = body.get("Description", "No Description Provided")
    price = body.get("Price", 0.00)
    nutrition_info = body.get("Nutrition Info","No Nutrition Info Provided")
    new_snack = Snack(name = name, description = description, price = price, nutrition_info = nutrition_info)

    try:
        new_snack.save()
        return JsonResponse({"Status Code": "200"})
    except:
        return JsonResponse({"Status Code": "500"})


@csrf_exempt
def createCart(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user = body.get("User", "No user Provided")
    total_price = body.get("Total Price", 0.00)
    num_items  = body.get("Num Items", "No Description Provided")
    
    new_cart = Cart(user = user, total_price = total_price, num_items = num_items)
    try:
        new_cart.save()
        return JsonResponse({"Status Code": "200", "NameTest": request.POST})
    except:
        return JsonResponse({"Status Code": "500"})


@csrf_exempt
def createWishlist(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user = body.get("User", "No user Provided")
    total_price = body.get("Total Price", 0.00)
    num_items  = body.get("Num Items", "No Description Provided")
    
    new_wishlist = Wishlist(user = user, total_price = total_price, num_items = num_items)
    try:
        new_wishlist.save()
        return JsonResponse({"Status Code": "200", "NameTest": request.POST})
    except:
        return JsonResponse({"Status Code": "500"})

def destroyUser(request,pk):
    try:
        user = User.objects.get(pk = pk)
        user.delete()
    except:
        return JsonResponse({"Status Code": "404"})

def destroySnack(request,pk):
    try:
        snack = Snack.objects.get(pk = pk)
        snack.delete()
    except:
        return JsonResponse({"Status Code": "404"})

def destroyCart(request,pk):
    try:
        cart = Cart.objects.get(pk = pk)
        cart.delete()
    except:
        return JsonResponse({"Status Code": "404"})

def destroyWishlist(request,pk):
    try:
        wishlist = Wishlist.objects.get(pk = pk)
        wishlist.delete()
    except:
        return JsonResponse({"Status Code": "404"})


def updateUser(request,pk):
    try:
        user, created = User.objects.update_or_create(
        pk=pk, defaults=request.body)
    except:
        return JsonResponse({"Status Code": "404"})


def updateSnack(request,pk):
    try:
        snack, created = Snack.objects.update_or_create(
        pk=pk, defaults=request.body)
    except:
        return JsonResponse({"Status Code": "404"})

def updateCart(request,pk):
    try:
        cart, created = Cart.objects.update_or_create(
        pk=pk, defaults=request.body)
    except:
        return JsonResponse({"Status Code": "404"})

def updateWishlist(request,pk):
    try:
        wishlist, created = Wishlist.objects.update_or_create(
        pk=pk, defaults=request.body)
    except:
        return JsonResponse({"Status Code": "404"})

