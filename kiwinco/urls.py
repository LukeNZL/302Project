from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
#from .views import UserLogin

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
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('<str:catagory>/', views.catagory, name='catagory'),
    path('addToCart/<int:item_id>', views.addToCart, name='addToCart'),
    path('removeFromCart', views.removeFromCart, name='removeFromCart'),
    path('buyCart', views.buyCart, name='buyCart'),
    path('buyItem/<int:item_id>', views.buyItem, name='buyItem'),
    path('success/', views.success, name='success'),
    path('successC/', views.successC, name='successC'),
    path('cancel/', views.cancel, name='cancel'),
    path('webhook/', views.webhook, name='webhook'),
    
    #path('login/', UserLogin.as_view(), name='login'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#landing page, logged in page