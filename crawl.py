import os

from sklearn.feature_extraction.text import HashingVectorizer

from common import File
from database import DBProvider
from datamodel import FileInfo

batch_size = 3
vectorizer = HashingVectorizer(n_features=1000)
db = DBProvider(clear_database=True)

class MemoryFile(File):
    def __init__(self, file_path_object):
        self.path = file_path_object.path
        self.name = file_path_object.name

        raw_content = self.load_content(file_path_object)
        self.content = raw_content.lower()
        self.coeffs = self.process(self.content)

    @staticmethod
    def load_content(file_path_object):
        file = open(file_path_object.path, 'r', encoding="utf8")
        return file.read()

    @staticmethod
    def process(file_content):
        return vectorizer.fit_transform([file_content]).tocsr()

    def distance(self, other_file):
        distance = self.coeffs.dot(other_file.coeffs.transpose())
        return distance


def get_batch_paths(root_path):
    paths = []
    for root, _, files in os.walk(root_path):
        for file_name in files:
            if len(paths) >= batch_size:
                break

            file_path = root + '\\' + file_name
            paths.append(File(file_path, file_name))

    return paths


def map_to_sql(file):
    entity = FileInfo()
    entity.filepath = file.path
    entity.filename = file.name
    entity.set_vector(file.coeffs)
    return entity


def commit_to_db(files):
    entities = list(map(lambda file: map_to_sql(file), files))
    db_session = db.get_session()
    db_session.add_all(entities)
    db_session.commit()


def run(root_path, _batch_size, _n_features):

    batch_size = _batch_size
    vectorizer = HashingVectorizer(n_features=_n_features)

    paths = get_batch_paths(root_path)
    files = list(map(lambda s: MemoryFile(s), paths))

    commit_to_db(files)
    return
