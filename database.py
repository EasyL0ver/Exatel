import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datamodel import Base


class DBProvider(object):
    def __init__(self, clear_database):
        #for testing
        if clear_database and os.path.exists('data.db'):
            print('Clearing database')
            os.remove('data.db')

        self.db = create_engine('sqlite:///data.db')
        self.active_session = None

        Base.metadata.create_all(self.db)

    def get_session(self):
        if not self.active_session:
            DBSession = sessionmaker(bind=self.db)
            self.active_session = DBSession()
        return self.active_session
