from database import DBProvider
from datamodel import FileInfo, Cluster
from sklearn.cluster import KMeans
from scipy.sparse import vstack, hstack
from common import File

batch_size = 4
db = DBProvider(clear_database=False)
means = KMeans(n_clusters=2, init='k-means++', max_iter=100)


class VectorizedFile(File):
    def __init__(self, file_info):
        super().__init__(file_info.filepath, file_info.filename)
        self.file_info = file_info
        self.vector = file_info.get_vector()


def run():
    cluster_session = db.get_session()

    all_file_infos = cluster_session.query(FileInfo).filter(FileInfo.cluster_id == None).limit(batch_size).all()

    print("Loaded: " + str(len(all_file_infos)) + ' file infos')

    vectorized_files = list(map(lambda info: VectorizedFile(info), all_file_infos))

    vectors = list(map(lambda m: m.vector, vectorized_files))
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

run()
