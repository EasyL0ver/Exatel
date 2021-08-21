# About

This is a submission for a Exatel's task in HackYeah 2019 hackathon concerning text files clustering. Solution was finished within 24 hour time limit with a team of two.


# Running the solution

use "pip install -r requirements.txt" to install python dependencies
execute "run.py" for example usage
database with results will be created after first execution

# Project details
	
The Python script created allows to cluster large amounts of random text data scraped from 
publicly available websites (pastebin etc.). Program input is a system path from which it will 
move upward the directory tree while parameterizing and clustering text files.
Hashing vectorization is employed to allow text file parameterization in very large data-set without performance drawbacks.
Optimal amount of clusters is calculated by applying the silhouette method to a small data subset.
Multidimensional K-means clustering is used to group the files with the most similar ones.
Program output is written to SQLite database or is printed in the console.
Database lets user to keep context without program running and batch the work, currently after processing files are moved
to organized folder next to the project root.

# Technology used

The script is writen entirely in python with usage of following modules (requirments.txt file):
* SQLAlchemy==1.3.8
* numpy==1.16.2
* scikit-learn==0.21.3
* scipy==1.2.1
* sklearn==0.0
* matplotlib=3.0.2

SQLAlchemy is an ORM software which allows simple integration with locally stored SQLite database
