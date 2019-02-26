# This script was written by Yogev Cohen,
# As a part of my Digital Humanities project.
# ************************************************************
# script order:
# 1. open us_movies.csv
# 2. open title_principals_only_actors.tsv
# 3. open wikidata_aa_actors and wikidata_aa_filmactors records.
# (Those files were created with wikidata-query helper service).
# 4. create new dataframe, appending to it num of total movies
# and num of movies with aa-actors in each year.
# 5. write the new dataframe to a csv file called year_movies_moviesWithAAActors.csv
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

#iterate over principals file and find all actors ids by unique movie tconst
def getActorsIdsByTconst(tconst):
	actors_ids = []
	for df in principals_file_dflist:
		matching_tconst_rows = df.loc[df['tconst'] == tconst]
		if matching_tconst_rows.shape[0] > 0:
			actors_ids += matching_tconst_rows['nconst'].tolist()
	return actors_ids

#by wikidata african american actors/film actors records, check wether an actor is african american
def checkIfAfricanAmericanActor(nconst):
	check_wikidata_aa_actors = wikidata_aa_actors.loc[wikidata_aa_actors['IMDb_ID'] == nconst]
	check_wikidata_aa_film_actors = wikidata_aa_film_actors.loc[wikidata_aa_film_actors['IMDb_ID'] == nconst]
	if (check_wikidata_aa_actors.shape[0] > 0 or check_wikidata_aa_film_actors.shape[0] > 0):
		return True
	return False

#returns total num of movies in certain year, and num of movies with african american actors
def findNumOfMoviesWithAfricanAmericanActorsInYear(year):
	num_of_movies = 0
	movies_in_year = movies.loc[movies['startYear'] == year]
	total_num = movies_in_year.shape[0]
	for (index,(tconst,primaryTitle,startYear,genres)) in movies_in_year.iterrows():
		movie_actors = getActorsIdsByTconst(tconst)
		for actor in movie_actors:
			if(checkIfAfricanAmericanActor(actor)):
				num_of_movies = num_of_movies+1
				break
	return (total_num,num_of_movies)

#the new data frame for the output.
year_movies_moviesWithAAActors = pd.DataFrame(columns=['year','num_of_movies','num_of_movies_with_AAActors'])

earliest_year = movies['startYear'].min()
current_year = 2019

#iterating over each year, find num of total movies and num of movies with aa-actors in each year.
for year in range(earliest_year,current_year):
	(num_of_movies,num_of_movies_with_AAActors) = findNumOfMoviesWithAfricanAmericanActorsInYear(year)
	year_movies_moviesWithAAActors = year_movies_moviesWithAAActors.append({'year':year,'num_of_movies':num_of_movies,'num_of_movies_with_AAActors':num_of_movies_with_AAActors},ignore_index=True)

#write the requested data to a new csv file.
year_movies_moviesWithAAActors.to_csv('year_movies_moviesWithAAActors.csv',encoding='utf-8',index=False)