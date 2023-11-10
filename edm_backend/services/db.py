import pandas as pd

from config import SQL_ALCHEMY_URI

from sqlalchemy import create_engine


class AppDb:
    def __init__(self):
        self.engine = None
        if SQL_ALCHEMY_URI:
            self.engine = create_engine(SQL_ALCHEMY_URI, isolation_level='AUTOCOMMIT', pool_size=10)