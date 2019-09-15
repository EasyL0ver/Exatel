from datamodel import FileInfo
from database import DBProvider
from sklearn.cluster import KMeans
from common import VectorizedFile
from scipy.sparse import vstack, hstack
from sklearn.metrics import silhouette_samples, silhouette_score

import numpy as np

db = DBProvider(clear_database=False)
aval_clusters_range = range(5, 10)
elbow_set_size_range = 30


def run():
    elbow_session = db.get_session()
    elbow_set = elbow_session.query(FileInfo).filter(FileInfo.cluster_id == None).limit(elbow_set_size_range).all()
    vectorized_files = list(map(lambda info: VectorizedFile(info), elbow_set))
    vectors = list(map(lambda m: m.vector, vectorized_files))
    silhouette_sample = []

    if len(vectors) <= 1:
        print("Invalid batch size or all files are clustered")
        return

    stacked_matrix = vstack(vectors)

    for size in aval_clusters_range:
        means = KMeans(n_clusters=size)
        labels = means.fit_predict(stacked_matrix)
        avg_silhouette = silhouette_score(stacked_matrix, labels)
        silhouette_sample.append(avg_silhouette)

    max_index = np.argmax(silhouette_sample)

    return aval_clusters_range[max_index]


