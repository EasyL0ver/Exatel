from scipy.sparse import vstack

from common import VectorizedFile
from datamodel import FileInfo, Cluster


def run(batch_size, means, cluster_session, n_clusters):
    all_file_infos = cluster_session.query(FileInfo).filter(FileInfo.cluster_id == None).limit(batch_size).all()

    print("Loaded: " + str(len(all_file_infos)) + ' file infos')

    vectorized_files = list(map(lambda info: VectorizedFile(info), all_file_infos))

    vectors = list(map(lambda m: m.vector, vectorized_files))

    if len(vectors) <= n_clusters:
        print("Invalid batch size or all files are clustered")
        return

    stacked_matrix = vstack(vectors)

    means.fit(stacked_matrix)

    cluster_entities = list(map(lambda center_vector: Cluster(center_vector), means.cluster_centers_))
    cluster_session.add_all(cluster_entities)

    for vectorized_file in vectorized_files:
        cluster_decision = means.predict(vectorized_file.vector)[0]
        correct_entity = cluster_entities[cluster_decision]
        vectorized_file.file_info.cluster = correct_entity

    cluster_session.commit()
    return
