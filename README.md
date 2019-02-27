# My Digital Humanities mini project.

# African-American actors in the US movie industry data analysis.
The project idea is to find out african-american actors in the US movie industry status and changes over the years.

# Project website:
https://yogco2.wixsite.com/aa-movie-actors-yogi

# How to run the scripts(windows):

* You should have python 3.6.x or higher and pandas library installed.
* wikidata_actor_africanamericans_imdbid.csv and wikidata_filmactor_africanamericans_imdbid.csv were created ahead with wikidata-query service, contains records of movie actors of african-american ethnicity.
* Scripts runtime may be very long because of very large datasets files.
* Each script file contains instructions for needed files and their location.

1. From IMDb-datasets page (https://www.imdb.com/interfaces/), download files: 
    title.basics.tsv.gz and title.principals.tsv.gz (table columns are described in the link)

2. From Kaggle-The Movies Dataset page (https://www.kaggle.com/rounakbanik/the-movies-dataset), download:
    movies_metadata.csv (table columns are described in the link)
    
3. Download all python scripts, wikidata_actor_africanamericans_imdbid.csv and wikidata_filmactor_africanamericans_imdbid.csv files from wikidata directory to same directory with the scripts.

4. Open cmd in python scripts directory.

5. Run python createTitlePrincipalsOnlyActors.py in order to create principals table of only actors records:
title_principals_only_actors.tsv file (which basicly contains imdb_id's of movies and their actors imdb_id's).

6. Run python createUsMovies.py in order to create a table of movies produced in the US:
us_movies.csv file (which contains id, title, release year and genres of every movie).

7. Run python createYearMoviesMoviesWithAAActors.py
It iterates over the years and for each year, counts the total number of movies produced and the number of those with african-american actors.
Finally writing the requested data to year_movies_moviesWithAAActors.csv file.

8. Run python createGenresPopularity.py
It will iterate over all african-american actors from records of wikidata query created files,
and for every actor, find his movies, find movie genres for every movie and add every genre to the genre count.
Finally writing the data to genre_num_of_movies.csv file.

# The final results:
* year_movies_moviesWithAAActors.csv file contains year - number of movies - number of movies with african-american actors (from earliest year in the db to 2018).
* genre_num_of_movies.csv file contains genre - number of movies from this genre (of only movies with african-american actors).

# Final tables and graphs:
These were created manually from the final results files described above.

# The result data may be inaccurate because of missing data in the movies-datasets, or lack of information about more african-american actors ethnic group in wiki-data records.
