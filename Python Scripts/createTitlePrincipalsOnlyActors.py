# This script was written by Yogev Cohen,
# As a part of my Digital Humanities project.
# ************************************************************
# the script:
# 1. open imdb-dataset/title.principals.tsv file for reading
# (title.principals.tsv contains the principal cast/crew for titles)
# 2. creating new title_principals_onlyactors.tsv file
# the new file contains only records of actors or actresses.
# ************************************************************
# The data.tsv file from compressed file title.principals.tsv.gz
# should be extracted to same folder and renamed as title_principals.tsv
# ************************************************************
# Information courtesy of
# IMDb
# (http://www.imdb.com).
# Used with permission.

import csv

# reading from the original tsv file, writing only actors or actresses records to a new file
with open('title_principals_only_actors.tsv','w+',encoding="utf8",newline='') as w:
	writer = csv.writer(w,delimiter='\t')
	with open('title_principals.tsv',encoding="utf8") as f:
		reader = csv.reader(f,delimiter='\t')
		for row in reader:
			if row[3] == 'actor' or row[3] == 'actress':	
				writer.writerow(row)