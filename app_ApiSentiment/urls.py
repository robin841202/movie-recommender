from django.contrib import admin
from django.urls import path
from app_ApiSentiment import views

#app_name='namesapce_app_ApiSentiment'

# 開放給大家用的api_get_sentiment/
urlpatterns = [
    path('', views.api_get_sentiment, name='api_get_sentiment'),
]
