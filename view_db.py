from database import DBProvider
from datamodel import FileInfo


def run():
    db = DBProvider(clear_database=False)
    all_files = db.get_session().query(FileInfo).filter(FileInfo.cluster_id != None).order_by(FileInfo.cluster_id).all()

    print('Printing content of database')
    for file in all_files:
        print(file)

    return


run()