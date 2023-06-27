from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
#from .views import UserLogin

###WIP###
from kiwinco.views import (
    CreateCheckoutSessionView,
    ProductPurchase,
    SuccessView,
    CancelView,
    stripe_webhook,
    StripeIntentView,
    CartPurchase,
    CreateCheckoutSessionViewCart,
    StripeIntentViewCart
)
###WIP###

urlpatterns = [
    path('', views.home, name='home'),
    path('kiwinco/', views.home, name='kiwinco'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('account/', views.accountPage, name='account'),
    path('delete/', views.deleteAccount, name='deleteuser'),
    path('edit/', views.editAccount, name='edituser'),

    path('register/', views.registerPage, name='register'),
    path('<int:item_id>/', views.item, name='item'),

    path('addToCart/<int:item_id>', views.addToCart, name='addToCart'),
    path('removeFromCart', views.removeFromCart, name='removeFromCart'),
    path('buyCart', views.buyCart, name='buyCart'),
    path('buyItem/<int:item_id>', views.buyItem, name='buyItem'),
#    path('success/', views.success, name='success'),
#    path('successC/', views.successC, name='successC'),
#    path('cancel/', views.cancel, name='cancel'),
#    path('webhook/', views.webhook, name='webhook'),
    
    #path('login/', UserLogin.as_view(), name='login'),

    ###WIP###

    path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('create-payment-intent-cart/', StripeIntentViewCart.as_view(), name='create-payment-intent-cart'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('payment/<int:pk>/', ProductPurchase.as_view(), name='payment'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('CartPurchase/', CartPurchase.as_view(), name='CartPurchase'),
    path('create-checkout-session-cart/', CreateCheckoutSessionViewCart.as_view(), name='create-checkout-session-cart'),

    path('<str:catagory>/', views.catagory, name='catagory'),
    ###WIP###

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#landing page, logged in page