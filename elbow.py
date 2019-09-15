import numpy as np
from scipy.sparse import vstack
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from common import VectorizedFile
from datamodel import FileInfo


def run(elbow_session, aval_clusters_range, elbow_set_size_range):
    elbow_set = elbow_session.query(FileInfo).filter(FileInfo.cluster_id == None).limit(elbow_set_size_range).all()
    vectorized_files = list(map(lambda info: VectorizedFile(info), elbow_set))
    vectors = list(map(lambda m: m.vector, vectorized_files))
    silhouette_sample = []

    if len(vectors) <= 1:
        print("Invalid batch size or all files are clustered")
        return

    stacked_matrix = vstack(vectors)

    for size in aval_clusters_range:
        if len(vectors) <= size:
            raise Exception('Vector size must be at least equal to number of clusters')

        means = KMeans(n_clusters=size)
        labels = means.fit_predict(stacked_matrix)
        avg_silhouette = silhouette_score(stacked_matrix, labels)
        silhouette_sample.append(avg_silhouette)

    max_index = np.argmax(silhouette_sample)

    return aval_clusters_range[max_index]


