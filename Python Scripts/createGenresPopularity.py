# This script was written by Yogev Cohen,
# As a part of my Digital Humanities project.
# ************************************************************
# script order:
# 1. create all genres dictionary
# 2. open us_movies.csv
# 3. open title_principals_only_actors.tsv
# 4. open wikidata_aa_actors and wikidata_aa_filmactors records.
# (Those files were created with wikidata-query helper service).
# 5. concat wikidata records to one dataframe
# 6. for each african-american actor, find his movies, find each movie genres
# and increment appropriate key-value in genres_dict
# 5. create a dataframe from genres_dict and write it to a csv file called genre_num_of_movies.csv.csv
# ************************************************************
# Files location instructions:
# us_movies.csv file created by createUsMovies.py,
# title_principals_only_actors.tsv file created by createTitlePrincipalsOnlyActors.py,
# wikidata_actor_africanamericans_imdbid.csv,
# and wikidata_filmactor_africanamericans_imdbid.csv created by wikidata-query,
# all should be in same dir with this script.
# ************************************************************
# Information courtesy of
# IMDb
# (http://www.imdb.com).
# Used with permission.

import pandas as pd

genres_dict = {'Drama':0,
'Comedy':0,
'Romance':0,
'Crime':0,
'Action':0,
'Thriller':0,
'Horror':0,
'Adventure':0,
'Documentary':0,
'Mystery':0,
'Sci-Fi':0,
'Fantasy':0,
'Family':0,
'Biography':0,
'Music':0,
'Western':0,
'History':0,
'Musical':0,
'War':0,
'Film-Noir':0,
'Animation':0,
'Sport':0,
'News':0}

#open us_movies.csv into a dataframe and make startYear column as int.
movies = pd.read_csv("us_movies.csv",dtype={'tconst':str,'primaryTitle':str,'startYear':str,'genres':str})
movies['startYear'] = pd.to_numeric(movies['startYear'],errors='coerce')
movies.dropna(subset=['startYear'],inplace=True)
movies['startYear'] = movies['startYear'].astype('int64')

#open title_principals_only_actors.tsv file which contains imdb-id of a movie,
#and imdb-id of the actors playing in that movie.
#It is more efficient to read it in chunks beacuse of it's very large.
principals_file_dflist = []
for chunk in pd.read_csv("title_principals_only_actors.tsv",delimiter='\t',chunksize=10**6):
	principals_file_dflist.append(chunk)

#open african american actors and filmactors(from wikidata records) csv files
wikidata_aa_actors = pd.read_csv("wikidata_actor_africanamericans_imdbid.csv")
wikidata_aa_film_actors = pd.read_csv("wikidata_filmactor_africanamericans_imdbid.csv")

#concat two wikidata df's to not iterate actors twice
wikidata_concated = pd.concat([wikidata_aa_actors,wikidata_aa_film_actors]).drop_duplicates().reset_index(drop=True)
wikidata_concated.dropna(subset=['IMDb_ID'],inplace=True)

#returns a data frame of actor movies
def getActorMoviesByImdbid(imdb_id):
	actor_movies_df = pd.DataFrame(columns=['tconst','ordering','nconst','category','job','characters'])
	for df in principals_file_dflist:
		movies_from_current_df = df.loc[df['nconst'] == imdb_id]
		actor_movies_df = actor_movies_df.append(movies_from_current_df)
	return actor_movies_df

#returns a list of movie genres
def getMovieGenresByTconst(tconst):
	movie = movies.loc[movies['tconst'] == tconst]
	if movie.shape[0] > 0 :
		movie_genres = movie['genres'].get_values()
		movie_genres = movie_genres[0].split(",")
		return movie_genres
	return []

#iterate over all african american wikidata_concated actors
#for each actor, get actor movies
#for each movie, get movie genres and increment genre key-value in genre_dict
for (index,(actor_page_link,actor_name,imdb_id)) in wikidata_concated.iterrows():
	actor_movies = getActorMoviesByImdbid(imdb_id)
	for (index,(tconst,ordering,nconst,category,job,characters)) in actor_movies.iterrows():
		genres = getMovieGenresByTconst(tconst)
		for genre in genres:
			genres_dict[genre] += 1

#creating a dataframe from genre_dict values and write it to a csv file.
genres_popularity_df = pd.DataFrame.from_dict(genres_dict,orient='index',columns=['num_of_movies'])
genres_popularity_df.index.name = 'genre'
genres_popularity_df.to_csv('genre_num_of_movies.csv',encoding='utf-8')
