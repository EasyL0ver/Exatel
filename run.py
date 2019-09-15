from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import HashingVectorizer

import cluster
import crawl
import silhouette
import view_db
from database import DBProvider


path = './sample_data'
crawl_batch_size = 30000
vectorizer = HashingVectorizer(n_features=1000)
db = DBProvider(clear_database=True)
n_cluster_range = range(5, 10)
elbow_set_size = 30
max_iterations = 100
cluster_batch_size = 1000
print_db = False


crawl.run(path, crawl_batch_size, vectorizer, db.get_session())
n_clusters = silhouette.run(db.get_session(), n_cluster_range, elbow_set_size)
cluster_means = KMeans(n_clusters=n_clusters, init='k-means++')
cluster.run(cluster_batch_size, cluster_means, db.get_session(), n_clusters=n_clusters)

if print_db:
    view_db.run(db.get_session())
