class File:
    def __init__(self, path, name):
        self.path = path
        self.name = name


class VectorizedFile(File):
    def __init__(self, file_info):
        super().__init__(file_info.filepath, file_info.filename)
        self.file_info = file_info
        self.vector = file_info.get_vector()
