from django.urls import path, include
from . import views

urlpatterns = [
    path('channel/<channel_code>/topics', views.business, name='business_home_page'),
    path('channel/<channel_code>/products', views.products, name='products'),
]