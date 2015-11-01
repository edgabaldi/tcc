import sqlitedict
import tempfile

class MySqliteDict(sqlitedict.SqliteDict):

    def __del__(self):
        try:
            super(MySqliteDict, self).__del__()
        except:
            pass

class SQLiteCacheBackend(object):

    def __init__(self):
        _, self.fname = tempfile.mkstemp(suffix='.db')
        self.cache = MySqliteDict(self.fname, autocommit=True)

    def __del__(self):
        import os
        try:
            os.remove(self.fname)
        except:
            pass

    def __setitem__(self, key, value):
        self.cache[key] = value

    def __getitem__(self, key):
        return self.cache[key]
