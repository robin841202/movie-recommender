from django.shortcuts import render

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import sequence
import pickle
import jieba

jieba.set_dictionary('app_ApiSentiment/jieba_big_chinese_dict/dict.txt.big')

# 關閉GPU
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# tensorflow內定的graph物件 缺少這，後面model.predict()會出錯
#  raise ValueError("Tensor %s is not an element of this graph." % obj)
#  ValueError: Tensor Tensor("dense_9/Softmax:0", shape=(?, 2), dtype=float32) is not an element of this graph.
# Django與tensorflow整合的問題(算是臭蟲bug)
import tensorflow as tf
from tensorflow.keras import backend as k
graph = tf.compat.v1.get_default_graph()

# 載入詞索引模型
tokenizer = pickle.load(open('app_ApiSentiment/sentiment_model/model_MLP/my_tokenizer.pickle', 'rb'))

# 載入tensorflow分類模型
model = load_model('app_ApiSentiment/sentiment_model/model_MLP/my_MLP_model.h5')
#model = load_model('app_ApiSentiment/sentiment_model/model_CNN/my_CNN_model.h5')

# ajax呼叫的API
from django.http import  JsonResponse
import json

# POST方式才需要。單獨指定這一支程式忽略csrf驗證。
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def api_get_sentiment(request):
    # 一律以json格式輸入與輸出
    print(request.content_type)
    print(request.body)

    # 這樣讀取會出錯 因為格式問題
    # print(request.POST.get('input_text'))

    # 讀取json格式
    received_json = json.loads(request.body)
    #print(received_json['input_text'])
    new_text = received_json['input_text']
    print(new_text)
    sentiment_prob = get_sentiment_proba(new_text)
    return JsonResponse(sentiment_prob)

# 大家都會呼叫的方法: 可取得情緒正面負面的機率值
def get_sentiment_proba( new_text ):
    tokens = jieba.lcut(new_text, cut_all=False)
    tokens = [tokens]
    #print(tokens)
    new_text_seq = tokenizer.texts_to_sequences(tokens)
    new_text_pad = sequence.pad_sequences(new_text_seq, maxlen= 150)
    # result = model.predict(new_text_pad) # 這樣寫會報錯
    # 報錯訊息: .... is not an element of this graph.
    # tensorflow 的模型 graph
    with graph.as_default():
       result = model.predict(new_text_pad)
    return  {'負面': round(float(result[0, 0]), 2), '正面': round(float(result[0, 1]), 2)}

print("app_ApiSentiment--深度學習情緒分類API模組載入成功!")