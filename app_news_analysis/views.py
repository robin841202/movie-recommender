from django.shortcuts import render


from django.http import  JsonResponse

def api_get_cat_topkey(request):

    cat = request.GET.get('news_category')
    topk = request.GET.get('topk')
    print(cat, topk)
    if topk:  # 不是空的字串 其結果才為True
        topk = int(topk)
    else:
        topk = 10  # 若使用者沒有輸入此值，內定為

    if cat:  # 不是空的字串 其結果才為True  也就是cat !=''
        content, wf_pairs = get_category_topkey(cat, topk)
    else:  # 否則回傳空的資料回去
        content = []
        wf_pairs = []
    return JsonResponse(
        {'chartdata': content,
         'wf_pairs': wf_pairs,
        } )


def chart_topkey(request):

    return render(request,
                  'app_news_analysis/chart_topkey.html')



import pandas as pd
df_data = pd.read_excel('app_news_analysis/dataset_news/中央社news_topkey_by_category.xlsx')

def get_category_topkey(category='科技', topk=10):
    keys = df_data.loc[ df_data['category'] == category ]
    wf_pairs = eval(  keys['top_keys'].values[0]  )
    wf_pairs = wf_pairs[0:topk]
    words = [w for w,f in wf_pairs]
    freqs = [f for w,f in wf_pairs]
    content = {
        "category": category,
        "labels": words,
        "values": freqs }
    return  content, wf_pairs



