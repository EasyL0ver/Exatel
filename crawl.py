import os

from common import File
from datamodel import FileInfo


class MemoryFile(File):
    def __init__(self, file_path_object, vectorizer):
        self.path = file_path_object.path
        self.name = file_path_object.name
        self.vectorizer = vectorizer

        raw_content = self.load_content(file_path_object)
        self.content = raw_content.lower()
        self.coeffs = self.process(self.content)

    @staticmethod
    def load_content(file_path_object):
        file = open(file_path_object.path, 'r', encoding="utf8")
        return file.read()

    def process(self, file_content):
        return self.vectorizer.fit_transform([file_content]).tocsr()

    def distance(self, other_file):
        distance = self.coeffs.dot(other_file.coeffs.transpose())
        return distance


def get_batch_paths(root_path, batch_size):
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


def commit_to_db(files, db_session):
    entities = list(map(lambda file: map_to_sql(file), files))
    db_session.add_all(entities)
    db_session.commit()


def run(root_path, batch_size, vectorizer, db_session):
    print('Crawling from the root path: {}, file batch size: {}'.format(root_path, batch_size))
    paths = get_batch_paths(root_path, batch_size)

    files = [None] * len(paths)
    for i in range(0, len(paths)):
        try:
            files[i] = MemoryFile(paths[i], vectorizer)
        except:
            print('Something went wrong when trying to load file: {}'.format(paths[i].name))

    commit_to_db(files, db_session)

    print('Finished crawling: {} files'.format(len(paths)))
    return
