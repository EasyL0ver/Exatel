from database import DBProvider
from datamodel import FileInfo


def run(db_session):
    all_files = db_session.query(FileInfo).filter(FileInfo.cluster_id != None).order_by(FileInfo.cluster_id).all()

    print('Printing content of database')
    for file in all_files:
        print(file)

    return


