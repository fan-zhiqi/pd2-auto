from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class CPLDBConnection:
    def __init__(self):
        engine = create_engine('postgresql://postgres:postgres@k8s-test-1.aamcn.com.cn:32100/cpl_service')
        DBsession = sessionmaker(bind=engine)
        self.dbsession = DBsession()