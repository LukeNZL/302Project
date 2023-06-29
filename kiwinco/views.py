import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Item, CartedItem, Purchase
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from.forms import RegisterForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import stripe, json
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime


import requests
# Create your views here.

def loginPage(request):
    #if "login" in request.POST:  # add the name "login" in your html button
    if request.method == 'POST':
        if "login" in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            
            url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/login/'
            data = {
                "email": email,
                "password": password,
                    
            }

            
            response = requests.post(url, data=data)
            #print(response.json())
            token=response.json().get('jwt')
            #print("************************************token" )
            #print(token)
            request.session['jwt'] = token
            if response.status_code == 200: 
                token = request.session.get('jwt')

                url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/user/'
                headers = {
                    'Authorization': token
                }
                
                
                userdata=requests.get(url, headers=headers)
                #print("************************************" )
                user = userdata.json() 
                user['logged_in'] = True

                print(user)
                
               
                messages.add_message(request, messages.INFO, user.get('username') + ' logged in successfully')
                return render(request, 'kiwinco/home.html', {'user': user})

                #messages.add_message(request, messages.INFO, 'User logged in successfully')
            else:
                messages.error(request, 'An error occurred during login attempt')
                return redirect('login')
           
    return render(request,'kiwinco/login.html')
        
def registerPage(request):
    if request.method == 'POST':
        #if "register" in request.POST:  # add the name "register" in your html button
        form = RegisterForm(request.POST)
        #print(form.data)
        if form.is_valid():
            # Get the user input from the request
            #username = request.POST.get('username')
            #password = request.POST.get('password')
            username = form.data['username']
            password = form.data['password1']
            email = form.data['email']
            
            #POST request to create a new user
            url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/create/'  # Replace with your API endpoint
            data = {
                'username': username,
                'email': email,
                'password': password,
                
            }
            response = requests.post(url, data=data)
            
            if response.status_code == 201:
                messages.add_message(request, messages.INFO, 'User created successfully')
                # User created successfully
                return redirect('home')
            elif response.status_code == 400:
                messages.add_message(request, messages.INFO, 'There is already an existing account for the provided email, try again')
                return redirect('home')
            else:
                messages.add_message(request, messages.INFO, 'UNKNOWN ERROR')
                return redirect('home')

        
        else:
            # Error creating user
            messages.error(request, 'An error occurred during registration, please ensure you are using a valid email address and password')

    return render(request, 'kiwinco/register.html')



def accountPage(request):
    
    token = request.session.get('jwt')

    url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/user/'
    headers = {
        'Authorization': token
    }
    
    userdata=requests.get(url, headers=headers)
    if userdata.status_code == 200:
        user = userdata.json()
        user['logged_in'] = True

        print(user)
        ##cart##
        if user['logged_in']==True:
            cart = CartedItem.objects.filter(buyerId = user['id'])
            total = sum(cart.values_list('price', flat=True))
            context=dict()
            context['cart']=cart
            context['total'] = "{0:.2f}".format(total/100)
        ##cart##
        context['user'] = user
        return render(request, 'kiwinco/account.html', context)
    else:
        # Handle the error appropriately
        error_message = 'Unable to retrieve user data. You may not be logged in Please try again later.'
        return render(request, 'kiwinco/error.html', {'error_message': error_message})
def deleteAccount(request):
    
    token = request.session.get('jwt')

    url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/delete/'
    headers = {
        'Authorization': token
    }
    
    userdata=requests.post(url, headers=headers)
    print(userdata)
    if userdata.status_code == 200:
        #user = userdata.json()
        #return render(request, 'kiwinco/account.html', {'user': user})
        messages.add_message(request, messages.INFO, 'User Deleted successfully')
        del request.session['jwt']
        return render(request, 'kiwinco/home.html')

    else:
        # Handle the error appropriately
        error_message = 'Unable to delete account.'
        return render(request, 'kiwinco/error.html', {'error_message': error_message})
def editAccount(request):
    token = request.session.get('jwt')
    url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/user/'
    headers = {
        'Authorization': token
    }
    
    userdata=requests.get(url, headers=headers)
    user = userdata.json()
    if userdata.status_code == 200:
        user['logged_in'] = True
   
    if request.method == 'POST':
        #if "register" in request.POST:  # add the name "register" in your html button
        form = RegisterForm(request.POST)
        print("###################################")
        print(form.data)
        if form.is_valid():
            
            # Get the user input from the request
            username = form.data['username']
            password = form.data['password1']
            email = form.data['email']
            
            #POST request to create a new user
            url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/edit/'  # Replace with your API endpoint
            data = {
                'username': username,
                'email': email,
                'password': password,
                
            }
            response = requests.put(url, data=data, headers=headers)
            print("response###################################")
            print(response)
            if response.status_code == 200:
                messages.add_message(request, messages.INFO, 'Your Details Have been Updated successfully')
                # User created successfully
                return redirect('account')
            elif response.status_code == 400:
                messages.add_message(request, messages.INFO, 'There is already an existing account for the provided email, try again')
                return redirect('account')
            else:
                messages.add_message(request, messages.INFO, 'UNKNOWN ERROR')
                return redirect('account')

    
        else:
            # Error updating user
            messages.error(request, 'An error occurred during Edit, please ensure you are using a valid email address and password')
    context=dict()
    ##cart##
    if user['logged_in']==True:
        cart = CartedItem.objects.filter(buyerId = user['id'])
        total = sum(cart.values_list('price', flat=True))

        context['cart']=cart
        context['total'] = "{0:.2f}".format(total/100)
    ##cart##
    context['user'] = user

    return render(request, 'kiwinco/accountedit.html',context)


def home(request):
    
    
    token = request.session.get('jwt')
    url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/user/'
    headers = {
        'Authorization': token
    }
    
    userdata=requests.get(url, headers=headers)
    print(userdata)
    user = userdata.json()
    user['logged_in'] = False

    if userdata.status_code == 200:
        user['logged_in'] = True

    print(userdata)
    print (user)
   
    #context = {'user': user}
    
    shirt_list = Item.objects.filter(Shirt = True)[:7]
    jumper_list = Item.objects.filter(Jumper_Jacket=True)[:7]
    pants_list = Item.objects.filter(Pants=True)[:7]
    featured_list = Item.objects.filter(Featured=True)[:7]

    #user=None
    ##search##
    if request.method == 'GET':
        if "search" in request.GET:
            search_value = request.GET['search']
            return redirect('/' + search_value)
    ##search##

    ## login ##
   
          
            """form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'An error occurred during registration')"""

       

            
            
            
            """username = request.POST.get('username').lower()
            password = request.POST.get('password')

            try:
                user = User.objects.get(username=username)
            except:
                messages.error(request, 'User does not exist')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username or password does not exist')"""
    ## login ##

    context = { 'shirt_list':shirt_list, 'jumper_list':jumper_list, 'pants_list':pants_list, 'featured_list':featured_list}

    ##cart##
    if user['logged_in']==True:
        cart = CartedItem.objects.filter(buyerId = user['id'])
        total = sum(cart.values_list('price', flat=True))

        context['cart']=cart
        context['total'] = "{0:.2f}".format(total/100)
    ##cart##
    context['user'] = user
    
   
    #return render(request, 'kiwinco/home.html',{'user': user})
    return render(request, 'kiwinco/home.html',context)

def item(request, item_id):
    token = request.session.get('jwt')

    url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/user/'
    headers = {
        'Authorization': token
    }
    
    userdata=requests.get(url, headers=headers)
    user = userdata.json()
    user['logged_in'] = False

    if userdata.status_code == 200:
        user['logged_in'] = True
    
    
    item = get_object_or_404(Item, pk=item_id)

    ##search##
    if request.method == 'GET':
        if "search" in request.GET:
            search_value = request.GET['search']
            return redirect('/' + search_value)
    ##search##

    context = {'item': item}

    ##cart##
    if user['logged_in']==True:
        cart = CartedItem.objects.filter(buyerId = user['id'])
        total = sum(cart.values_list('price', flat=True))

        context['cart']=cart
        context['total'] = "{0:.2f}".format(total/100)
    ##cart##
    context['user'] = user

    return render(request, 'kiwinco/item.html', context)

def catagory(request,catagory):

    token = request.session.get('jwt')

    url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/user/'
    headers = {
        'Authorization': token
    }
    
    userdata=requests.get(url, headers=headers)
    user = userdata.json()
    user['logged_in'] = False

    if userdata.status_code == 200:
        user['logged_in'] = True
    item_list = Item.objects.order_by('created')

    sort_value = 'Newest-Release'


    ##search##
    if request.method == 'GET':
        if "search" in request.GET:
            search_value = request.GET['search']
            return redirect('/' + search_value)
        
    ##search##

    if 'sort_value' in request.GET:
        if (request.GET['sort_value'] == 'Oldest-Release'):
            item_list = Item.objects.order_by('-created')
            sort_value = 'Oldest-Release'
        elif (request.GET['sort_value'] == 'Price-low-to-high'):
            item_list = Item.objects.order_by('Price')
            sort_value = 'Price-low-to-high'
        elif (request.GET['sort_value'] == 'Price-high-to-low'):
            item_list = Item.objects.order_by('-Price')
            sort_value = 'Price-high-to-low'
        else:
            item_list = Item.objects.order_by('created')
            sort_value = 'Newest-Release'

    if (catagory == 'Shirts'):
        item_list = item_list.filter(Shirt = True)
    elif(catagory == 'Jumpers'):
        item_list = item_list.filter(Jumper_Jacket=True)
    elif (catagory == 'Pants'):
        item_list = item_list.filter(Pants=True)
    elif (catagory == 'Featured'):
        item_list = item_list.filter(Featured=True)
    else:
        item_list = item_list.filter(ItemName__contains=catagory)
        catagory = 'Search Result: "' + catagory + '"'


    context = {'catagory': catagory, 'item_list': item_list, 'sort_value': sort_value,}

    ##cart##
    if user['logged_in']==True:
        cart = CartedItem.objects.filter(buyerId = user['id'])
        total = sum(cart.values_list('price', flat=True))

        context['cart']=cart
        context['total'] = "{0:.2f}".format(total/100)
    ##cart##
    context['user'] = user

    return render(request, 'kiwinco/catagory.html', context)

def logoutUser(request):
    token = request.session.get('jwt')

    url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/logout/'
    headers = {
        'Authorization': token
    }
    
    response = requests.post(url, headers=headers)
    context=dict()
    print(response)
    print(response.json())
    if response.status_code == 200:
        messages.add_message(request, messages.INFO, 'User logged out successfully')
        del request.session['jwt']
    else:
        messages.add_message(request, messages.INFO, 'Unable to logout user, try again')
        token = request.session.get('jwt')

        url = 'http://127.0.0.1:8000/api/user/'
        headers = {
            'Authorization': token
        }
        userdata=requests.get(url, headers=headers)
        print("************************************" )
        user = userdata.json()
        context={'user':user}
        return render(request, 'kiwinco/home.html', context)
    return render(request, 'kiwinco/home.html')

@csrf_exempt
def addToCart(request, item_id):
    token = request.session.get('jwt')

    url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/user/'
    headers = {
        'Authorization': token
    }
    
    userdata=requests.get(url, headers=headers)
    user = userdata.json()
    user['logged_in'] = False

    if userdata.status_code == 200:
        user['logged_in'] = True
        
        
        
    if request.method == "POST":
        if user['logged_in'] == True:
            x = CartedItem(price=request.POST['price'], itemId=item_id,buyerId = user['id'], itemSize=request.POST['size'], itemName=request.POST['name'])
            x.save()
            # i = Item.objects.get(pk=item_id)
            # if request.POST['size'] == 'XS':
            #     i.Stock_XS = i.Stock_XS-1
            # elif request.POST['size'] == 'S':
            #     i.Stock_S = i.Stock_S - 1
            # elif request.POST['size'] == 'M':
            #     i.Stock_M = i.Stock_M - 1
            # elif request.POST['size'] == 'L':
            #     i.Stock_L = i.Stock_L - 1
            # elif request.POST['size'] == 'XL':
            #     i.Stock_XL = i.Stock_XL - 1
            # i.save()
        else:
            messages.error(request, 'Must be logged in to cart items')
    return redirect("/" + str(item_id))

@csrf_exempt
def removeFromCart(request):
    u = CartedItem.objects.get(id=request.POST.get('id'))
    u.delete()
    return render(request, 'kiwinco/home.html')
    return redirect('/1')


def buyCart(request):
    token = request.session.get('jwt')

    url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/user/'
    headers = {
        'Authorization': token
    }
    
    userdata=requests.get(url, headers=headers)
    user = userdata.json()
    user['logged_in'] = False

    if userdata.status_code == 200:
        user['logged_in'] = True
        
    if user['logged_in'] == True:

        cart = CartedItem.objects.filter(buyerId = user['id'])
        total = sum(cart.values_list('price', flat=True))

        YOUR_DOMAIN = "http://127.0.0.1:8001/"
        stripe.api_key = 'sk_test_51N60CYJDzpA491w35DvXhdahCcOasic85U3T2UETDLPRrvtmAWkFhEThfq5HVGLYwUcAZ8LbwVeOgZGFfRFb6rus00GArPVxXL'

        try:
            checkout_session = stripe.checkout.Session.create(
                billing_address_collection='auto',
                shipping_address_collection={
                #"name": user['username'],
                'allowed_countries': ['NZ'],
                },
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        #'price': 'price_1N6eFXJDzpA491w3wbEEK3GH',
                        'price_data': {
                            'currency': 'nzd',
                            'product_data' : {
                                'name' : "Cart",
                            },
                            'unit_amount' : total,

                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/successC',
                cancel_url=YOUR_DOMAIN + '/cancel',
                automatic_tax={'enabled': True},
        )
        except Exception as e:
            return HttpResponse(e)
        messages.add_message(request, messages.INFO, 'Payment Cancelled')
        return redirect(checkout_session.url, code=303)
    
    else:
        return('home')


    #     u = CartedItem.objects.filter(buyerId=request.user.id)
    #     for i in u:
    #         j = Item.objects.get(pk=i.itemId)
    #         if i.itemSize == 'XS':
    #             j.Stock_XS = j.Stock_XS-1
    #         elif i.itemSize == 'S':
    #             j.Stock_S = j.Stock_S - 1
    #         elif i.itemSize == 'M':
    #             j.Stock_M = j.Stock_M - 1
    #         elif i.itemSize == 'L':
    #             j.Stock_L = j.Stock_L - 1
    #         elif i.itemSize == 'XL':
    #             j.Stock_XL = j.Stock_XL - 1
    #         x = Purchase(price=i.price, buyerId=request.user.id, itemSize=i.itemSize, itemName=i.itemName)
    #         x.save()
    #         j.save()
    #         i.delete()
    # return redirect('home')

#@csrf_exempt
def buyItem(request, item_id):




    # item = get_object_or_404(Item, pk=item_id)
    # #context = {'item': item}

    # YOUR_DOMAIN = "http://127.0.0.1:8001/kiwinco/"
    # stripe.api_key = 'sk_test_51N60CYJDzpA491w35DvXhdahCcOasic85U3T2UETDLPRrvtmAWkFhEThfq5HVGLYwUcAZ8LbwVeOgZGFfRFb6rus00GArPVxXL'

    # try:
    #     checkout_session = stripe.checkout.Session.create(
    #         billing_address_collection='auto',
    #         shipping_address_collection={
    #           'allowed_countries': ['NZ'],
    #         },
    #         line_items=[
    #             {
    #                 # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
    #                 #'price': 'price_1N6eFXJDzpA491w3wbEEK3GH',
    #                 'price_data': {
    #                     'currency': 'nzd',
    #                     'product_data' : {
    #                         'name' : item.ItemName,
    #                     },
    #                     'unit_amount' : item.Price,

    #                 },
    #                 'quantity': 1,
    #             },
    #         ],
    #         mode='payment',
    #         success_url=YOUR_DOMAIN + 'success',
    #         cancel_url=YOUR_DOMAIN + 'cancel',
    #         automatic_tax={'enabled': True},
    # )
    # except Exception as e:
    #     return HttpResponse(e)

    # return redirect(checkout_session.url, code=303) 
    
    #return render(request, 'kiwinco/purchase.html', context)




    # if request.user.is_authenticated:

    #     u = Item.objects.get(id=request.POST['id'])
    #     if request.POST['size'] == 'XS':
    #         u.Stock_XS = u.Stock_XS-1
    #     elif request.POST['size'] == 'S':
    #         u.Stock_S = u.Stock_S - 1
    #     elif request.POST['size'] == 'M':
    #         u.Stock_M = u.Stock_M - 1
    #     elif request.POST['size'] == 'L':
    #         u.Stock_L = u.Stock_L - 1
    #     elif request.POST['size'] == 'XL':
    #         u.Stock_XL = u.Stock_XL - 1
    #     x = Purchase(price=u.Price, buyerId=request.user.id, itemSize=request.POST['size'], itemName=u.ItemName)
    #     x.save()
    #     u.save()

    return redirect('home')


def create_checkout_session(request):
    #TEMP!!!!!!
    YOUR_DOMAIN = "http://127.0.0.1:8001/"
    stripe.api_key = 'sk_test_51N60CYJDzpA491w35DvXhdahCcOasic85U3T2UETDLPRrvtmAWkFhEThfq5HVGLYwUcAZ8LbwVeOgZGFfRFb6rus00GArPVxXL'

    try:
        checkout_session = stripe.checkout.Session.create(
            billing_address_collection='auto',
            shipping_address_collection={
              'allowed_countries': ['NZ'],
            },
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    #'price': 'price_1N6eFXJDzpA491w3wbEEK3GH',
                    'price_data': {
                        'currency': 'nzd',
                        'product_data' : {
                            'name' : 'temp',
                        },
                        'unit_amount' : 1000,

                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + 'kiwinco/success',
            cancel_url=YOUR_DOMAIN + 'kiwinco/cancel',
            automatic_tax={'enabled': True},
    )
    except Exception as e:
        return HttpResponse(e)

    return redirect(checkout_session.url, code=303)

def success(request):

    return render(request, 'success.html')

def successC(request):
    token = request.session.get('jwt')

    url = 'http://127.0.0.1:8000/api/user/'
    headers = {
        'Authorization': token
    }
    
    userdata=requests.get(url, headers=headers)
    user = userdata.json()
    if userdata.status_code == 200:
        user['logged_in'] = True
        
    if user['logged_in'] == True:

        u = CartedItem.objects.filter(buyerId=user['id'])
        for i in u:
            j = Item.objects.get(pk=i.itemId)
            if i.itemSize == 'XS':
                j.Stock_XS = j.Stock_XS-1
            elif i.itemSize == 'S':
                j.Stock_S = j.Stock_S - 1
            elif i.itemSize == 'M':
                j.Stock_M = j.Stock_M - 1
            elif i.itemSize == 'L':
                j.Stock_L = j.Stock_L - 1
            elif i.itemSize == 'XL':
                j.Stock_XL = j.Stock_XL - 1
            x = Purchase(Price=i.price, buyerId=user['id'], itemSize=i.itemSize, itemName=i.itemName)
            x.save()
            j.save()
            i.delete()
    return render(request, 'kiwinco/success.html')

def cancel(request):
    return render(request, 'kiwinco/cancel.html')


stripe.api_key = 'sk_test_51N60CYJDzpA491w35DvXhdahCcOasic85U3T2UETDLPRrvtmAWkFhEThfq5HVGLYwUcAZ8LbwVeOgZGFfRFb6rus00GArPVxXL'


###WIP###

import json
import stripe
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View


#stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_key = 'sk_test_51N60CYJDzpA491w35DvXhdahCcOasic85U3T2UETDLPRrvtmAWkFhEThfq5HVGLYwUcAZ8LbwVeOgZGFfRFb6rus00GArPVxXL'

class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class ProductPurchase(TemplateView):
    template_name = "purchase.html"

    def get_context_data(self, **kwargs):

        token = self.request.session.get('jwt')
        url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/user/'
        headers = {
            'Authorization': token
        }
        
        userdata=requests.get(url, headers=headers)
        print(userdata)
        user = userdata.json()
        user['logged_in'] = False

        if userdata.status_code == 200:
            user['logged_in'] = True

        print(userdata)
        print (user)

        item = Item.objects.get(id=self.kwargs["pk"])
        context = super(ProductPurchase, self).get_context_data(**kwargs)
        context.update({
            "item": item,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })

        ##cart##
        if user['logged_in']==True:
            cart = CartedItem.objects.filter(buyerId = user['id'])
            total = sum(cart.values_list('price', flat=True))

            context['cart']=cart
            context['total'] = "{0:.2f}".format(total/100)
        ##cart##

        context['user'] = user
        return context
    

class CartPurchase(TemplateView):
    template_name = "purchasecart.html"

    def get_context_data(self, **kwargs):

        token = self.request.session.get('jwt')
        url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/user/'
        headers = {
            'Authorization': token
        }
        
        userdata=requests.get(url, headers=headers)
        print(userdata)
        user = userdata.json()
        user['logged_in'] = False

        if userdata.status_code == 200:
            user['logged_in'] = True

        print(userdata)
        print (user)


        context = super(CartPurchase, self).get_context_data(**kwargs)


        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        context['user'] = user
        ##cart##
        if user['logged_in']==True:
            cart = CartedItem.objects.filter(buyerId = user['id'])
            total = sum(cart.values_list('price', flat=True))

            context['cart']=cart
            context['total'] = "{0:.2f}".format(total/100)
        ##cart##        

        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):

        token = self.request.session.get('jwt')
        url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/user/'
        headers = {
            'Authorization': token
        }

        userdata=requests.get(url, headers=headers)
        print(userdata)
        user = userdata.json()
        

        product_id = self.kwargs["pk"]
        item = Item.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8001"
        checkout_session = stripe.checkout.Session.create( 
            payment_method_types=['card'],
            line_items=[
                {                     
                    'price_data': {
                        'currency': 'nzd',
                        'unit_amount': 1,
                        'product_data': {
                            'name': item.ItemName,
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                    "product_id": item.ItemName,
                    "Address" : "WIP",
                },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
    

class CreateCheckoutSessionViewCart(View):
    def post(self, request, *args, **kwargs):

        token = self.request.session.get('jwt')
        url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/user/'
        headers = {
            'Authorization': token
        }

        userdata=requests.get(url, headers=headers)
        print(userdata)
        user = userdata.json()


        cart = CartedItem.objects.filter(buyerId = user['id'])
        total = sum(cart.values_list('price'))

        total = "{0:.2f}".format(total)

        YOUR_DOMAIN = "http://127.0.0.1:8001"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'nzd',
                        'unit_amount': total,
                        'product_data': {
                            'name': 'cart',
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                    "product_id": 'str(cart_names)', 
                },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]
        Address = session["metadata"]["Address"]


        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. " + str(product_id),
            recipient_list=[customer_email],
            from_email="test@test.com"
        )

        send_mail(
            subject="Purchase Made",
            message=f"Purchase from " + customer_email + " of " + str(product_id) + " to " + str(Address),
            recipient_list=["test@test.com"],
            from_email="test@test.com"
        )
    
    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)


        customer_email = stripe_customer['email']
        product_id = intent["metadata"]["product_id"]
        Address = intent["metadata"]["Address"]
        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered." + str(product_id),
            recipient_list=[customer_email],
            from_email="test@test.com"
        )

        send_mail(
            subject="Purchase Made",
            message=f"Purchase from " + customer_email + " of " + str(product_id) + " to " + str(Address),
            recipient_list=["test@test.com"],
            from_email="test@test.com"
        )

    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            address_dict = req_json['address']

            address = address_dict['line1'] + ' ' + address_dict['line2'] + ' ' + address_dict['city'] + ' ' + address_dict['country'] + ' ' + address_dict['postal_code'] + ' ' + address_dict['state']

            product_id = self.kwargs["pk"]
            item = Item.objects.get(id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=item.Price,
                currency='nzd',
                automatic_payment_methods={
                'enabled': True,
                },
                customer=customer['id'],
                metadata={
                    "product_id": item.ItemName,
                    "Address" : str(address),
                },    
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({ 'error': str(e) })
        


class StripeIntentViewCart(View):
    def post(self, request, *args, **kwargs):
        try:
            token = self.request.session.get('jwt')
            url = 'http://kiwinco-userapi-dev.ap-southeast-2.elasticbeanstalk.com/api/user/'
            headers = {
                'Authorization': token
            }

            userdata=requests.get(url, headers=headers)
            print(userdata)
            user = userdata.json()
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            address_dict = req_json['address']

            address = address_dict['line1'] + ' ' + address_dict['line2'] + ' ' + address_dict['city'] + ' ' + address_dict['country'] + ' ' + address_dict['postal_code'] + ' ' + address_dict['state']
            print(address)
            cart = CartedItem.objects.filter(buyerId = user['id'])
            total = sum(cart.values_list('price', flat=True))
            carted_items = cart.values_list('itemName', flat = True)
            carted_size = cart.values_list('itemSize', flat = True)
                
            
            cart_names = {}

            for i in range (len(cart)):
                temp = ""    
                temp = str(carted_items[i]) + str(carted_size[i])
                cart_names[str(i)] = temp
            
            cart_final = ""

            for i in range (len(cart)):
                cart_final += cart_names[str(i)]  
                cart_final += ' '
            

            intent = stripe.PaymentIntent.create(
                amount=total,
                currency='nzd',
                automatic_payment_methods={
                'enabled': True,
                },
                customer=customer['id'],
                metadata={
                    "product_id": str(cart_final), 
                    "Address" : str(address),
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({ 'error': str(e) })
        

###WIP###