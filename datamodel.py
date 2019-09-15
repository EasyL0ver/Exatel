import io
import sqlite3

from pylab import *
from scipy.sparse import csr_matrix
from sqlalchemy import Column, Integer, String, BLOB, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import deferred, relationship

Base = declarative_base()


class FileInfo(Base):
    __tablename__ = 'file_infos'
    id = Column(Integer, primary_key=True)
    filepath = Column(String(128), nullable=False)
    filename = Column(String(128), nullable=False)

    vector = deferred(Column(BLOB(250000), nullable=False))

    cluster_id = Column(Integer, ForeignKey("clusters.id"), nullable=True)
    cluster = relationship("Cluster")

    def __str__(self):
        return 'File named: {} assigned to cluster: {}'.format(self.filename, self.cluster_id)

    def set_vector(self, coeffs):
        c = coeffs.todense()
        out = io.BytesIO()
        np.save(out, c)
        out.seek(0)
        self.vector = sqlite3.Binary(out.read())

    def calc_distance(self, other_coefficients):
        distance = self.get_vector().dot(other_coefficients.transpose())
        return distance

    def get_vector(self):
        out = io.BytesIO(self.vector)
        out.seek(0)
        output = np.load(out).astype(float64)
        sparse_output = csr_matrix(output)
        return sparse_output


class Cluster(Base):
    __tablename__ = 'clusters'

    id = Column(Integer, primary_key=True)

    center = deferred(Column(BLOB(250000), nullable=False))

    def __init__(self, center_vector):
        self.set_center(center_vector)

    def get_center(self):
        out = io.BytesIO(self.center)
        out.seek(0)
        output = np.load(out).astype(float64)
        sparse_output = csr_matrix(output)
        return sparse_output

    def set_center(self, coeffs):
        out = io.BytesIO()
        np.save(out, coeffs)
        out.seek(0)
        self.center = sqlite3.Binary(out.read())


