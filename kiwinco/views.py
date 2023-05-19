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
import stripe
from django.core.mail import send_mail
# Create your views here.

def home(request):
    shirt_list = Item.objects.filter(Shirt = True)[:7]
    jumper_list = Item.objects.filter(Jumper_Jacket=True)[:7]
    pants_list = Item.objects.filter(Pants=True)[:7]
    featured_list = Item.objects.filter(Featured=True)[:7]

    form = RegisterForm()

    ##search##
    if request.method == 'GET':
        if "search" in request.GET:
            search_value = request.GET['search']
            return redirect('/kiwinco/' + search_value)
    ##search##

    ## login ##
    if request.method == 'POST':
        if "register" in request.POST:  # add the name "register" in your html button
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'An error occurred during registration')

        if "login" in request.POST:  # add the name "login" in your html button
            username = request.POST.get('username').lower()
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
                messages.error(request, 'Username or password does not exist')
    ## login ##

    context = { 'shirt_list':shirt_list, 'jumper_list':jumper_list, 'pants_list':pants_list, 'featured_list':featured_list, 'form': form}

    ##cart##
    if request.user.is_authenticated:
        cart = CartedItem.objects.filter(buyerId = request.user.id)
        total = sum(cart.values_list('price', flat=True))

        context['cart']=cart
        context['total'] = total
    ##cart##

    return render(request, 'kiwinco/home.html', context)

def item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    form = RegisterForm()

    ##search##
    if request.method == 'GET':
        if "search" in request.GET:
            search_value = request.GET['search']
            return redirect('/kiwinco/' + search_value)
    ##search##


    ## login ##
    if request.method == 'POST':
        if "register" in request.POST:  # add the name "register" in your html button
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'An error occurred during registration')

        if "login" in request.POST:  # add the name "login" in your html button
            username = request.POST.get('username').lower()
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
                messages.error(request, 'Username or password does not exist')
    ## login ##

    context = {'item': item, 'form': form}

    ##cart##
    if request.user.is_authenticated:
        cart = CartedItem.objects.filter(buyerId = request.user.id)
        total = sum(cart.values_list('price', flat=True))

        context['cart']=cart
        context['total'] = total
    ##cart##

    return render(request, 'kiwinco/item.html', context)

def catagory(request,catagory):

    form = RegisterForm()

    item_list = Item.objects.order_by('created')

    sort_value = 'Newest-Release'


    ##search##
    if request.method == 'GET':
        if "search" in request.GET:
            search_value = request.GET['search']
            return redirect('/kiwinco/' + search_value)
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

    ## login ##
    if request.method == 'POST':
        if "register" in request.POST:  # add the name "register" in your html button
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'An error occurred during registration')

        if "login" in request.POST:  # add the name "login" in your html button
            username = request.POST.get('username').lower()
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
                messages.error(request, 'Username or password does not exist')
    ## login ##

    context = {'catagory': catagory, 'item_list': item_list, 'sort_value': sort_value, 'form': form}

    ##cart##
    if request.user.is_authenticated:
        cart = CartedItem.objects.filter(buyerId = request.user.id)
        total = sum(cart.values_list('price', flat=True))

        context['cart']=cart
        context['total'] = total
    ##cart##

    return render(request, 'kiwinco/catagory.html', context)

# def registerPage(request):
#     form = RegisterForm()
#
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'An error occurred during registration')
#
#     return render(request, 'kiwinco/home.html', {'form': form})



# def loginPage(request):
#
#     if request.method == 'POST':
#         username = request.POST.get('username').lower()
#         password = request.POST.get('password')
#
#         try:
#             user = User.objects.get(username=username)
#         except:
#             messages.error(request, 'User does not exist')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Username or password does not exist')
#     context = {'page': page}
#
#     return render(request, 'kiwinco/home.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

@csrf_exempt
def addToCart(request, item_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            x = CartedItem(price=request.POST['price'], itemId=item_id, buyerId=request.user.id, itemSize=request.POST['size'], itemName=request.POST['name'])
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
    if request.user.is_authenticated:

        cart = CartedItem.objects.filter(buyerId = request.user.id)
        total = sum(cart.values_list('price', flat=True))

        YOUR_DOMAIN = "http://127.0.0.1:8000/kiwinco/"
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
                                'name' : "Cart",
                            },
                            'unit_amount' : total,

                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + 'successC',
                cancel_url=YOUR_DOMAIN + 'cancel',
                automatic_tax={'enabled': True},
        )
        except Exception as e:
            return HttpResponse(e)

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

    item = get_object_or_404(Item, pk=item_id)
    #context = {'item': item}

    YOUR_DOMAIN = "http://127.0.0.1:8000/kiwinco/"
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
                            'name' : item.ItemName,
                        },
                        'unit_amount' : item.Price,

                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + 'success',
            cancel_url=YOUR_DOMAIN + 'cancel',
            automatic_tax={'enabled': True},
    )
    except Exception as e:
        return HttpResponse(e)

    return redirect(checkout_session.url, code=303) 
    
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

    # return redirect('home')


def create_checkout_session(request):
    #TEMP!!!!!!
    YOUR_DOMAIN = "http://127.0.0.1:8000/"
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
    return render(request, 'kiwinco/success.html')

def successC(request):
    if request.user.is_authenticated:
        u = CartedItem.objects.filter(buyerId=request.user.id)
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
            x = Purchase(Price=i.price, buyerId=request.user.id, itemSize=i.itemSize, itemName=i.itemName)
            x.save()
            j.save()
            i.delete()
    return render(request, 'kiwinco/success.html')

def cancel(request):
    return render(request, 'kiwinco/cancel.html')


stripe.api_key = 'sk_test_51N60CYJDzpA491w35DvXhdahCcOasic85U3T2UETDLPRrvtmAWkFhEThfq5HVGLYwUcAZ8LbwVeOgZGFfRFb6rus00GArPVxXL'

@csrf_exempt
def webhook(request):
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
  
  if event['type'] == 'checkout.session.completed':
    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
    session = stripe.checkout.Session.retrieve(
    event['data']['object']['id'],
    expand=['line_items'],
    )

    customer_email = session["customer_details"]["email"]

    send_mail(
        subject = "KiwiNCo Purchace Completed",
        message = "Thank you for your purchace",
        recipient_list=[customer_email],
        from_email="adamts028@gmail.com"
    )

    send_mail(
        subject = "KiwiNCo Incoming Order",
        message = "Order",
        recipient_list=["adamts028@gmail.com"],
        from_email="adamts028@gmail.com"
    )

    line_items = session.line_items
    # Fulfill the purchase...
    #print(session)
    # fulfill_order(line_items)

  # Passed signature verification
  return HttpResponse(status=200)