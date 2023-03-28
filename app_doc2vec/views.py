from django.shortcuts import render
from django.http import JsonResponse
from gensim.models.doc2vec import Doc2Vec
import pandas as pd
df = pd.read_excel('app_doc2vec/dataset/中央社各類新聞.xlsx')
model = Doc2Vec.load("app_doc2vec/dataset/cna_news_strTag.model")

def index(request):
    return render(request, "app_doc2vec/document_analysis.html")


def api_cat_news(request):
    # cat='政治'
    cat = request.GET['category']
    content = get_cat_news(cat=cat)
    # print(content)
    return JsonResponse({"content": content})

def get_cat_news(cat="政治"):
    docs = []
    df_cat = df[df.category == cat]
    for i in range(len(df_cat)):
        content = {"id": df_cat.iloc[i].item_id, "category": df_cat.iloc[i].category, "title": df_cat.iloc[i].title,
                   "link": df_cat.iloc[i].link}
        docs.append(content)
    return docs[0:5]

#----------------------------------------------------------------------------------------------------------------------

def api_keywords_similar_news(request):
    tokens = request.POST['tokens']
    tokens = [t for t in tokens.split()]
    if len(tokens) == 0:
        tokens = ['台北市', '台灣']
    content = get_keywords_most_similar(tokens)
    return JsonResponse({"content": content})


def get_keywords_most_similar(tokens=['柯文', '台北']):
    new_vector = model.infer_vector(tokens)
    topdocs = model.docvecs.most_similar(positive=[new_vector], topn=5)
    docsim = []
    for item_id, score in topdocs:
        itemdf = df[df.item_id == item_id]
        title = itemdf.title.tolist()[0]
        content = itemdf.content.tolist()[0]
        category = itemdf.category.tolist()[0]
        link = itemdf.link.tolist()[0]
        score = round(score, 2)
        content = {"category": category, "title": title,
                   "link": link, "id": item_id, 'score': score}
        docsim.append(content)
    return docsim

#----------------------------------------------------------------------------------------------------------------------

def api_news_content(request):
    item_id = request.GET['news_id']
    content = get_news_content(item_id)
    related = get_news_most_similar_by_id(item_id)
    # print(related)
    return JsonResponse({"news_content": content, "related_news": related})

def get_news_content(item_id):
    itemdf = df[df.item_id == item_id]
    title = itemdf.title.tolist()[0]
    content = itemdf.content.tolist()[0]
    category = itemdf.category.tolist()[0]
    link = itemdf.link.tolist()[0]
    print(category, title)
    data = {"id": item_id, "category": category,
            "title": title, "content": content, "link": link}
    return data

def get_news_most_similar_by_id(item_id):
    topdocs = model.docvecs.most_similar(positive=[item_id], topn=3)
    docsim = []
    for item_id, score in topdocs:
        itemdf = df[df.item_id == item_id]
        title = itemdf.title.tolist()[0]
        content = itemdf.content.tolist()[0]
        category = itemdf.category.tolist()[0]
        link = itemdf.link.tolist()[0]
        score = round(score, 2)
        content = {"id": item_id, "category": category,
                   "title": title, "link": link, "score": score}
        docsim.append(content)
    return docsim




