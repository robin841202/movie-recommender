"""site_news_analysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from app_news_analysis import views
from app_keyword import views as views_kw

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  views_kw.keyword, name = 'call_keyword'  ),
    # path('chart_topkey/', views.chart_topkey, name = 'chart_topkey'   ),
    path('chart_topkey', views.chart_topkey, name='chart_topkey'),
    path('api_get_cat_topkey', views.api_get_cat_topkey, name='api_cat_topkey'),

    #文章推薦APP
    path('news_recmd/', include('app_doc2vec.urls')),
    #midtermAPP
    path('midterm/', include('app_midterm.urls')),
    #movieAPP
    path('movie/', include('app_movie.urls')),
    #callSentimentAPP
    path('getSentiment/', include('app_callSentimentApi.urls')),
    #apiSentimentAPP
    path('api_get_sentiment/', include('app_ApiSentiment.urls')),
]
