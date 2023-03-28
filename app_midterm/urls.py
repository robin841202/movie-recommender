from django.urls import path
from app_midterm import views

app_name="app_midterm"

urlpatterns=[
    path('',views.newsInfo, name="newsInfo"),
    path('showWordCloud/', views.showWordCloud, name='showWordCloud'),
    path('api_get_info', views.api_get_info, name='api_get_info'),
    path('api_get_cloud', views.api_get_cloud, name='api_get_cloud'),
]