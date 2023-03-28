from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from snownlp import SnowNLP
from bs4 import BeautifulSoup
from collections import Counter
import jieba.posseg
import requests

# Create your views here.
def newsInfo(request):
    return render(request, 'app_midterm/newsInfo.html')

def showWordCloud(request):
    return render(request, 'app_midterm/showWordCloud.html')

def api_get_cloud(request):
    content = request.GET.get('content')
    word_pos_pairs = jieba.posseg.lcut(content)
    topwords = word_frequency_pos(word_pos_pairs)

    return JsonResponse({'topwords':topwords})

def api_get_info(request):
    link = request.GET.get('news_link')
    try:
        r = requests.get(link)
        page = BeautifulSoup(r.text, 'lxml')
        title = page.find('h1', {'class': "article-title"}).text
        div_mainfigure = page.find('div', {'class': 'main-figure'})
        image_src = div_mainfigure.find('img')['src']
        div_article = page.find('div', {'class': "article-body"})
        p = div_article.findAll('p')
        content = ''
        for paragraph in p:
            content += paragraph.text
        snow = SnowNLP(content)
        top5sentences = snow.sentences[0:5]
        summary = snow.summary(5)
        word_pos_pairs = jieba.posseg.lcut(content)
        topwords = word_frequency_pos(word_pos_pairs)
        return JsonResponse({'title': title, 'image_src': image_src, 'top5sentences': top5sentences, 'summary': summary, 'topwords': topwords})
    except Exception as e:
        print(str(e))
        return JsonResponse({'errorThrown': str(e)})


def word_frequency_pos( wp_pairs ):
	filtered_words =[]
	pos_tokens =[]
	for word, pos in wp_pairs:
		if (len(word) >= 2):
			filtered_words.append((word,pos))
	counter = Counter( filtered_words) # 回傳這種格式 (('台灣', 'ns'), 11)
	for word_freq in counter.most_common(): #格式整理成tuple之後再回傳 ('台灣', 'ns', 11)
		pos_tokens.append( (word_freq[0][0], word_freq[0][1], word_freq[1]) )
	#return pos_tokens
	return pos_tokens