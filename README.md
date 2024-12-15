# CIS4930 Final Project: Movie Recommender

## Repo Layout
#### The `data` folder contains the raw data in the form of a CSV file
#### The `src` folder contains all the code for the project
- `main.py` is the driver of the project that runs the GUI. Run this file to run the program.
- `curate_data.py` holds the functions that cleaned the raw data.
- `model.py` contains the model functions. 

## Required Libraries
- Pandas
- Numpy
- Nicegui
- Requests
- Pywebview

## Brainstorm

Use CountVectorizer on a pool of metadata, create 1000x1000 matrix with similarity scores, searches must include at least a title. If there are more paramters than title, first find similarity based on title then filter that list by additional parameter(s). We want to store the matrix in a file, so it isn't computed every execution.

Plan:
For each movie in cleaned_dataset, combine all features into one metadata string
Use CountVectorizer to create a matrix where the columns are each movie and the rows are a word that appears at least once in metadata
Compute Cosine Similarity scores between each movie using the previously computed matrix, storing it in a new matrix that is # movies 
by # movies in size
Get 9 movies that have the highest similarity scores to given movie title. 
If there are other parameters entered in the search (genre, year, director), filter the already computed simlilar movies based on it.
-   Ex: If the information given was the title "Star Wars: A New Hope" and director "Steven Spielberg" then it would refine the number 
       of possbile recommendations to movies that were directed by Spielberg and sort them by the similarity score with the Star Wars title.

Create a GUI application that allows the user to enter criteria into a search bar, returned recommendations will include the movie poster
  image, title, and year. Additional functionality/presentation is TBD. 
In order to save time, the Cosine-Similarity matrix will be stored in a file and loaded upon each program execution.

#### References
- https://www.datacamp.com/tutorial/recommender-systems-python
- https://techvidvan.com/tutorials/movie-recommendation-system-python-machine-learning/
- https://towardsdatascience.com/basics-of-countvectorizer-e26677900f9c
- https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
- https://stackoverflow.com/questions/22586741/python-storing-a-large-matrix-into-a-text-file-for-later-usage

