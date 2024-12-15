from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

# get the curated dataset
df = pd.read_csv('../data/cleaned_dataset.csv')
unedited_df = pd.read_csv('../data/imdb_top_1000.csv')

# Create count vectorizer & count matrix to convert the text to vectors (each column is a word, each row is a movie)
# count = CountVectorizer(stop_words='english')
# count_matrix = count.fit_transform(df['soup'])

# # Calculate a numeric representation of similarity between 2 movies using cosine similarity between their words
# cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
# np.save('../data/cosine_similarity_matrix.npy', cosine_sim2)

# reset the index of the DF, and create a series of the data to get the indices of the movies
df = df.reset_index()
movie_name_indices = pd.Series(df.index, index=df['Series_Title'])

# load in the cosine similarity matrix
cosine_sim = np.load('../data/cosine_similarity_matrix.npy')

# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(title, filter, inp):
    title = title.lower()
    inp = str.lower(inp.replace(" ", ""))

    try:
        # Get the index of the movie that matches the title
        idx = movie_name_indices[title]
            
    except:
        message = ("Sorry, this movie is either not in the dataset or is misspelled")
        return np.array(["Error",message])

    try:
        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:]

        # List for final 9 best indices of movies
        movie_indices = []

        # Director
        if filter =="Director":
            for score in sim_scores:
                if df["Director"].iloc[score[0]] == inp:
                    movie_indices.append(score[0])
                    if len(movie_indices) >= 9:
                        break

        # Actor
        elif filter == "Actor":
            for score in sim_scores:
                if (df["Star1"].iloc[score[0]] == inp or 
                    df["Star2"].iloc[score[0]] == inp or 
                    df["Star3"].iloc[score[0]] == inp):
                    movie_indices.append(score[0])
                    if len(movie_indices) >= 9:
                       break

        # Genre
        elif filter == "Genre":
            inp = inp.title()
            for score in sim_scores:
                if inp in df["Genre"].iloc[score[0]]:
                    movie_indices.append(score[0])
                    if len(movie_indices) >= 9:
                        break
        
        # Year
        elif filter == "Year":
            for score in sim_scores:
                if df["Released_Year"].iloc[score[0]] == inp:
                    movie_indices.append(score[0])
                    if len(movie_indices) >= 9:
                        break

        # Just Name
        elif filter == "None":
            # Get the scores of the 9 most similar movies
            sim_scores = sim_scores[1:10]
            # Get the movie indices
            movie_indices = [i[0] for i in sim_scores]

        # If filter returned no results, its an error
        if len(movie_indices) == 0:
            raise KeyError

        # Return the top 9 most similar movies
        return df['Series_Title'].iloc[movie_indices]
    except KeyError:
        message = "Sorry, this filter value is either not in the dataset or is misspelled"
        return np.array(["Error",message])


def get_poster_link(index, title):
    api_key = os.getenv('API_KEY')
    title = title.replace(" ", "+")
    url = 'https://api.themoviedb.org/3/search/movie?query='+title+'&api_key='+api_key
    data = requests.get(url)
    data = data.json()
    poster_path = data['results'][0]["poster_path"]
    if type(poster_path) != str:
        return unedited_df['Poster_Link'].iloc[index]
    full_path = "https://image.tmdb.org/t/p/w500" + poster_path
    return full_path

def get_results_info(results):
    # results will be a pandas series
    indexes = results.index
    titles = results.array
    final_results = list()
    for i in range(titles.size):

        # create a movie dictionary that has attributes
        # could add more info if we want
        # 'genre' should be an array of strings
        movie = {
        'title': unedited_df['Series_Title'].iloc[indexes[i]],
        'year': unedited_df['Released_Year'].iloc[indexes[i]],
        'poster_link': get_poster_link(indexes[i], titles[i]),
        'imdb_rating': unedited_df['IMDB_Rating'].iloc[indexes[i]],
        'genre': unedited_df['Genre'].iloc[indexes[i]]
        }

        # add it to a list
        final_results.append(movie)

    # return numpy array with each element a dictionary entry
    return final_results