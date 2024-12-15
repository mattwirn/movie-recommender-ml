"""
Clean the dataset. Clean up the data and make sure 
the returned dataset has only the necessary features for training.
Pass in True to see missing-value stats (default=False).
"""

import pandas as pd

# import the dataset and create a dataframe
dataset = pd.read_csv('../data/imdb_top_1000.csv')
df = pd.DataFrame(dataset).copy()

# Function to convert all strings to lower case and strip names of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            if ',' in x:
                x = str.lower(x.replace(",", ""))
            if '.' in x:
                x = str.lower(x.replace(".", ""))
            return str.lower(x.replace(" ", ""))
        else:
            return ''
        
def clean_lower(x):
    if isinstance(x, list):
        return [str.lower(i) for i in x]
    else:
        if isinstance(x, str):
            if ',' in x:
                x = str.lower(x.replace(",", ""))
            if '.' in x:
                x = str.lower(x.replace(".", ""))
            return str.lower(x)
        else:
            return ''
        
def create_soup(x):
    return (x['Series_Title'] + ' ' + 
            x['Genre'] + ' ' + 
            x['Director'] + ' ' + 
            x['Star1'] + ' ' + 
            x['Star2'] + ' ' + 
            x['Star3'] + ' ' + 
            x['Overview'])


# drop unnecessary columns
curated_df = df.drop(labels=['Poster_Link', 'Certificate', 'Runtime', 'No_of_Votes', 'Star4', 'Gross'], axis=1)

# fill in the missing data with the mean value of Meta_score
meta_score_mean = curated_df["Meta_score"].mean().round()
curated_df["Meta_score"] = curated_df["Meta_score"].fillna(meta_score_mean)

# keep copy of director and genre columns so they can be preserved after making soup
titles = curated_df['Series_Title']
directors = curated_df['Director']
genres = curated_df['Genre']

features1 = ['Director', 'Star1', 'Star2', 'Star3']
for feature in features1:
    curated_df[feature] = curated_df[feature].apply(clean_data)

features2 = ['Series_Title', 'Genre', 'Overview']
for feature in features2:
    curated_df[feature] = curated_df[feature].apply(clean_lower)


# create the soup column, containing all the data we'll feed the vectorizer
curated_df['soup'] = curated_df.apply(create_soup, axis=1)

# drop duplicates (if any)
curated_df.drop_duplicates(inplace=True)

# reset director and genre columns
curated_df['Genre'] = genres
curated_df['Series_Title'] = titles

# make the movie titles and director names all lowercase
for index, title in enumerate(curated_df['Series_Title']):
    curated_df.loc[index, 'Series_Title'] = title.lower()
for index, director in enumerate(curated_df['Director']):    
    curated_df.loc[index, 'Director'] = director.lower()


curated_df.to_csv('../data/cleaned_dataset.csv', index=False)

# data is cleaned. yay!