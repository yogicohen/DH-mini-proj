# This script was written by Yogev Cohen,
# As a part of my Digital Humanities project.
# ************************************************************
# the script:
# 1. opens kaggle-the-movie-dataset/movies_metadata.csv file
# 2. creates a list of imdb-id's of movies produced in the US
# 3. opens imdb-dataset/title.basics.tsv file
# 4. with the help of the us-prod-list created, creates a new data frame
#    of movies produced in the us, with the columns : tconst,primaryTitle,startYear,genres
# 5. creates "us_movies.csv" from the dataframe in step 4
# ************************************************************
# movies_metadata.csv file from kaggle/the-movie-dataset.zip should be in same folder.
# title.basics.tsv.gz from imdb-dataset should be in same folder.
# ************************************************************
# Information courtesy of
# IMDb
# (http://www.imdb.com).
# Used with permission.

import pandas as pd
import ast

def us_in_production_countries(my_dictlist):
    if type(my_dictlist) is list:
    	for d in my_dictlist:
    		if (d['name'] == 'United States of America'):
    			return True
    return False

#load kaggle-the-movies-dataset/movies_metadata.csv file
movies_metadata_df = pd.read_csv("movies_metadata.csv",low_memory=False)

#create dataframe consists of only imdb-id and production-countries columns
#use that dataframe to create a list of imdb-id's of movies from United States of America
imdbid_prouctioncountries_df = movies_metadata_df[['imdb_id','production_countries']].copy()
imdbid_prouctioncountries_df.dropna(subset=['production_countries'],inplace=True)

#make 'production_countries' column appear as a list of dicts
imdbid_prouctioncountries_df.loc[:,'production_countries'] = imdbid_prouctioncountries_df.loc[:,'production_countries'].apply(lambda x: ast.literal_eval(x))

usprod_imdb_id_list = []

#extracting only imdb-id's of movies produced in the US to a list of imdb-id's
for (id,(imdb_id,production_countries)) in imdbid_prouctioncountries_df.iterrows():
	if (us_in_production_countries(production_countries)):
		usprod_imdb_id_list.append(imdb_id)

# ************************************************************

#load imdb-dataset/title.basics.tsv file
basics_df = pd.read_csv("title.basics.tsv.gz",compression = 'gzip', sep = '\t',dtype={'tconst':str,'titleType':str,'primaryTitle':str,'originalTitle':str,'isAdult':str,'startYear':str,'endYear':str,'runtimeMinutes':str,'genres':str})

#extract only titles that are of type movie and necessary columns
movies_df = basics_df.loc[basics_df['titleType'] == 'movie']
movies_df = movies_df[['tconst','primaryTitle','startYear','genres']]

us_movies_df = pd.DataFrame(columns=['tconst','primaryTitle','startYear','genres'])

#appending only entries of movies produced in the US
for (id,(tconst,primaryTitle,startYear,genres)) in movies_df.iterrows():
	if (tconst in usprod_imdb_id_list):
		us_movies_df = us_movies_df.append({'tconst':tconst,'primaryTitle':primaryTitle,'startYear':startYear,'genres':genres},ignore_index=True)

#create csv file 'us_movies'
us_movies_df.to_csv('us_movies.csv',encoding='utf-8',index=False)