import json
import requests_with_caching
def get_movies_from_tastedive(str1):
    baseUrl = "https://tastedive.com/api/similar"
    payload = {"q":str1, "type":"movies", "limit":"5" }
    r = requests_with_caching.get(baseUrl, params = payload)
    data = json.loads(r.text)
    return data

def extract_movie_titles(dict):
    lst1 = []
    for item in dict['Similar']['Results']:
        lst1.append(item['Name'])
    return lst1

def get_related_titles(lst2):
    lst3 = []
    for item in lst2:
        lst4 = extract_movie_titles(get_movies_from_tastedive(item))
        for item2 in lst4:
            if item2 not in lst3:
                lst3.append(item2)
    return lst3
    


def get_movie_data(str2):
    baseUrl = "http://www.omdbapi.com/"
    payload = {'t': str2, 'r': 'json'}
    r = requests_with_caching.get(baseUrl, params = payload)
    data = json.loads(r.text)
    return data

def get_movie_rating(dict):
    rating = 0
    for item in dict['Ratings']:
        if item['Source'] == 'Rotten Tomatoes':
            rating = int(item['Value'][:2])
    print(rating)
    return rating


def get_sorted_recommendations(lst):
    related_movies = get_related_titles(lst)
    ratings = []
    for movie in related_movies:
        ratings.append(get_movie_rating(get_movie_data(movie)))
    lot1 = zip(related_movies, ratings)
    lot2 = sorted(lot1, key = lambda l: (l[1],l[0]), reverse = True)
    print(lot2)
    sorted_list = []
    for item in lot2:
        sorted_list.append(item[0])
    return sorted_list
    

get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

