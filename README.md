# My Digital Humanities mini project.

# African-American actors in the US movie industry data analysis.
# How to use:

* You should have python 3.6.x or higher and pandas library installed. *

1. From IMDb-datasets page (https://www.imdb.com/interfaces/), download files: 
    title.basics.tsv.gz (table columns are described in the link)
    title.principals.tsv.gz (table columns are described in the link)

2. From Kaggle-The Movies Dataset page (https://www.kaggle.com/rounakbanik/the-movies-dataset), download:
    movies_metadata.csv (table columns are described in the link)
    
3. Run createTitlePrincipalsOnlyActors.py in order to create principals table of only actors records:
title_principals_only_actors.tsv file (which basicly contains imdb_id's of movies and their actors imdb_id's).

4. Run createUsMovies.py in order to create a table of movies produced in the US:
us_movies.csv file (which contains id, title, release year and genres of every movie).

5. Run createYearMoviesMoviesWithAAActors.py
It iterates over the years and for each year, counts the total number of movies produced and the number of those with african-american actors.
Finally writing the requested data to year_movies_moviesWithAAActors.csv file.

6. Run createGenresPopularity.py
It will iterate over all african-american actors from records of wikidata query created files,
and for every actor, find his movies, find movie genres for every movie and add every genre to the genre count.
Finally writing the data to genre_num_of_movies.csv file.

*** Steps 5 and 6 may take a lot of time because of very large datasets and inefficient implementation. ***

*** Each script file contains instructions for needed files and their location. ***
