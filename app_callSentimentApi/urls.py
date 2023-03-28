from django.urls import path
from app_callSentimentApi import views


app_name = 'namespace_app_callSentimentApi'

urlpatterns=[
    path('', views.index, name='index'),
]