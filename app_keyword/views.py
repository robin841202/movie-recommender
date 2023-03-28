from django.shortcuts import render


import pandas as pd
df = pd.read_excel('app_keyword/dataset_news/中央社各類新聞-切詞與頻率統計.xlsx')
news_categories=['政治','科技','運動','證卷','產經','娛樂','生活','國際','社會','文化','全部']

def keyword(request):
    # 第一次載入網頁時網頁端沒有傳送關鍵字 所有資料都設定為空值
    newslinks = []
    if request.method == 'POST': # 網頁端有傳送關鍵字
        key = request.POST['userkeyword']
        query_df = df[df['tokens'].str.contains(key)]
        #  查詢結果不是空的 進一步去取得你要的資料
        if len(query_df) != 0:
            newslinks = get_title_link(key)

    return render(request, 'app_keyword/keyword.html', {
        'newslinks': newslinks,
    })


#  取得新聞標題 連結 類別
def get_title_link( query_key ):
    query_df = df[df['tokens'].str.contains(query_key)]
    title_link =[]
    for i in range(query_df.shape[0]):
        c = query_df.iloc[i]['category']
        t = query_df.iloc[i]['title']
        l = query_df.iloc[i]['link']
        title_link.append((c,t,l))
    return title_link[0:10]