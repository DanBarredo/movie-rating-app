import urllib.parse
import json
import requests


class OMDBError(Exception):
    """OMDBError repsents an error returned by OMDb API"""
    pass
    

class Movie:

    def __init__(self, movie_data):
        """Creates a movie object."""

        self.omdb_data = movie_data

    def get_movie_title(self, source="Rotten Tomatoes"):
        """Gets movie title."""
        #breakpoint()

        return self.omdb_data["Title"]

    def get_movie_rating(self, source="Rotten Tomatoes"):
        """Gets movie rating"""
        for ratings in self.omdb_data["Ratings"]:
            if ratings["Source"] == source:
                return ratings["Value"]

        return f" -Wait- Rating for source {source} was not found."


class OMDB(object):
    def __init__(self, apikey):
        self.apikey = apikey

    def build_url(self, **kwargs):
        kwargs["apikey"] = self.apikey
        url = "http://www.omdbapi.com/?"
        url += urllib.parse.urlencode(kwargs)
        #breakpoint()
        return url

    def call_api(self, **kwargs):
        url = self.build_url(**kwargs)
        breakpoint()
        response = requests.get(url)
        response_data = response.json()
        breakpoint()
        if ("Error") in response_data:
            raise OMDBError(response_data["Error"])
            #breakpoint()
        return response_data

    def get_movie(self, movie_query):
        movie_data = self.call_api(t=movie_query)
        return Movie(movie_data)
        
    def search(self, movie_query):
        movie_dictionaries = self.call_api(s=movie_query)
        return movie_dictionaries["Search"]


def return_single_movie_object(movie_query):
    """Returns a single movie object."""

    apikey = get_apikey()
    #breakpoint()
    try:
        omdb = OMDB(apikey)
        my_movie_object = omdb.get_movie(movie_query)
        return my_movie_object
    except OMDBError as err:
        print("OMDBError: {0}".format(err))
        return    

def print_single_movie_rating(movie_title):
    """Prints a single movie title and rating as a string"""
    movie = return_single_movie_object(movie_title)
    print(f"The rating for \"{movie.get_movie_title()}\" is {movie.get_movie_rating()}")

def print_all_ratings(movie_list):
    """Prints movie list adn respective ratings"""
    for movie in movie_list:

        single_movie = return_single_movie_object(movie)
        #breakpoint()

        title = single_movie.get_movie_title()
        rating = single_movie.get_movie_rating()

        print(f"The movie, \"{title}\" has a rating of {rating}")

def list_search_results(movie_query):
    """Prints all movie titles in a movie list"""
    apikey = get_apikey()
    #breakpoint()
    try:
        omdb = OMDB(apikey)
        breakpoint()
        matching_movie_list = omdb.search(movie_query)
        
    except OMDBError as err:
        print("OMDBError: {0}".format(err))
        breakpoint()
        return
        
    movie_titles = [each_movie["Title"] for each_movie in matching_movie_list]

    for movie in movie_titles:
        print("    ", movie)

def get_apikey():
    """opens and gets api key from .txt file"""
    with open("omdb-api-key.txt") as api_key:
        key = api_key.read()
    key = key.strip()
    return key


def main():
    """ runs movie search or rating app """

    default_movie_list = ["Lost in Translation", "Black Dynamite", "Whiplash"]
    #breakpoint()
    print_all_ratings(default_movie_list)


    search_or_ratings = int(input("Would you like to search for a movie (1) or find the rating of a specific movie(2) :" ))
    while True:
        #breakpoint()

        if search_or_ratings == 1:
            movie_query = input("Enter a movie title: ")
            list_search_results(movie_query)
            #breakpoint()

            break

        elif search_or_ratings == 2:
            movie_query = input("Enter a movie title: ")
            print_single_movie_rating(movie_query)
            #breakpoint()

            break

        else:
            raise TypeError("Wrong input. It must be 1 or 2.")
# It tells Python to go directly to the main function and run that
if __name__ == "__main__":
    main()
