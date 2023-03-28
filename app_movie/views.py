from django.shortcuts import render
from django.http import JsonResponse
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_excel('app_movie/dataset/IMDB_top250_preprocessed.xlsx')
df = df.sort_values(by=['Year'], ascending=False)
#df.set_index('imdbID', inplace = True)
indices = pd.Series(df.imdbID)
print(indices)
# instantiating and generating the count matrix
countVec = CountVectorizer()
count_matrix = countVec.fit_transform(df['bag_of_words'])
# generating the cosine similarity matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)
page_contentNum = 12

print(cosine_sim.shape)

def moviesInfo(request):
    return render(request, "app_movie/moviesInfo.html")

def results(request):
    imdbID = request.GET.get('imdbID')
    target_movie = get_movie_by_id(imdbID)
    print("target movie", target_movie)
    recommend_moviesimdbID = recommendations(str(imdbID))
    movies_content = []
    for item in recommend_moviesimdbID:
        movie_content = get_movie_by_id(item[0])[0]
        movie_content.append(item[1])
        movies_content.append(movie_content)
    movies_content = json.dumps(movies_content)
    context = {
        'target_movie': target_movie[0],
        'movies_content': movies_content
    }
    return render(request, "app_movie/results.html", context)

def api_get_movies(request):
    page = request.GET['page']
    movies_content = get_movies_by_page(int(page))
    return JsonResponse({"movies_content": movies_content})

def api_get_pages(request):
    allMoviesCount = df.shape[0]
    pages = allMoviesCount/page_contentNum + 1
    return JsonResponse({"pages": pages})

def api_get_movie_by_title(request):
    movieTitle = request.GET['movieTitle']
    movie_content = get_movie_by_title(movieTitle)
    return JsonResponse({"movie_content": movie_content})

def api_search_by_title(request):
    searchTitle = request.GET['searchTitle']
    movies_content = search_by_title(searchTitle)
    return JsonResponse({"movies_content": movies_content})

def get_movies(movieNum):
    movies_df = df.iloc[:movieNum]
    moviesList = movies_df.values.tolist()
    #posterList = movies_df.Poster.tolist()
    #data = {"Title": titleList, "Poster": posterList}
    return moviesList

def get_movies_by_page(page):
    num = df.shape[0]
    last_page = num/page_contentNum + 1
    start = (page - 1) * page_contentNum
    if page == last_page:
        movies_df = df.iloc[start:]
    else:
        movies_df = df.iloc[start:start+page_contentNum]
    moviesList = movies_df.values.tolist()
    return moviesList

def get_movie_by_title(movieTitle):
    movies_df = df[df.Title == movieTitle]
    movie = movies_df.values.tolist()[0]
    return movie

def search_by_title(searchTitle):
    movies_df = df[df['Title'].str.contains(searchTitle)]
    if movies_df.empty:
        return ''
    else:
        movies = movies_df.values.tolist()
        return movies


def get_movie_by_id(id):
    movies_df = df[df.imdbID == id]
    movie = movies_df.values.tolist()
    return movie


# function that takes in movie title as input and returns the top 10 recommended movies
def recommendations(id, cosine_sim=cosine_sim):
    recommended_ids = []

    # gettin the index of the movie that matches the title
    idx = indices[indices == id].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)

    print(score_series)
    scores_over_tenpercent = score_series.iloc[1:21]
    print(scores_over_tenpercent)

    # getting the indexes of the recommended similar movies
    recommended_indexes = list(scores_over_tenpercent.index)

    # populating the list with the titles of the best 20 matching movies
    for i in recommended_indexes:
        print(i, df.loc[i,"imdbID"])
        recommended_ids.append(df.loc[i,"imdbID"])
    print("recommended ids", recommended_ids)
    print(df)
    recommended_movies = []
    for j in range(len(recommended_ids)):
        score = round(scores_over_tenpercent.values.tolist()[j] * 100)
        item = [recommended_ids[j], score]
        recommended_movies.append(item)
    return recommended_movies