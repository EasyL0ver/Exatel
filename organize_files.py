from datamodel import FileInfo

import os


def organize_files(db_session, organize_path):
    all_files = db_session.query(FileInfo).filter(FileInfo.cluster_id != None).filter(FileInfo.organized == False).order_by(FileInfo.cluster_id).all()

    if not os.path.exists(organize_path):
        os.mkdir(organize_path)

    for file in all_files:
        file_path = file.filepath
        target_path = organize_path + '/' + str(file.cluster_id)

        if not os.path.exists(target_path):
            os.mkdir(target_path)

        file_target_path = target_path + '/' + file.filename

        for retry in range(100):
            try:
                if os.path.exists(file_target_path):
                    os.remove(file_target_path)

                os.rename(file_path, file_target_path)
                break
            except:
                print
                "rename failed, retrying..."
        file.filepath = file_target_path
        file.organized = True
    db_session.commit()

