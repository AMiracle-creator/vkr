"""
URL configuration for diplom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import HomePage, predict, analytics_page, single_hotel_info, period_info, indetifier_form, age_form, \
    date_form

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('analytics/', analytics_page, name='analytics'),
    path('hotel_info/', single_hotel_info, name='hotel_info'),
    path('period_info/', period_info, name='period'),
    path('booking_prediction/', predict, name='prediction'),
    path('indetifier_form/', indetifier_form, name='hotel_info_form'),
    path('age_form/', age_form, name='age_info_form'),
    path('date_form/', date_form, name='date_info_form')
]
