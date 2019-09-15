import sys
import os
import crawl
import cluster
import elbow
from sklearn.feature_extraction.text import HashingVectorizer
from database import DBProvider

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))
#print('First argument:', sys.argv[0]);

g_path = './data/sample-data'
crawl.run(g_path, 3, 1000)
cluster.run(400, 2, 'k-means++', 100)
