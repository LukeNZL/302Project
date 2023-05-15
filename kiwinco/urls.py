from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    #path('register/', views.registerPage, name='register'),
    path('<int:item_id>/', views.item, name='item'),
    path('<str:catagory>/', views.catagory, name='catagory'),
    path('addToCart/<int:item_id>', views.addToCart, name='addToCart'),
    path('removeFromCart', views.removeFromCart, name='removeFromCart'),
    path('buyCart', views.buyCart, name='buyCart'),
    path('buyItem', views.buyItem, name='buyItem'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)