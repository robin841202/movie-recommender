from django.urls import path
from app_doc2vec import views

app_name="app_news_rcmd"

urlpatterns=[
    path('',views.index, name="index"),
    path('api_cat_news',views.api_cat_news,name="api_cat_news"),
    path('api_keywords_similar_news',views.api_keywords_similar_news,name="api_keywords_similar_news"),
    path('api_news_content',views.api_news_content, name="api_news_content"),
]