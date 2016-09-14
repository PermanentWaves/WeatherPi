import MySQLdb


class Db:

    con = False

    def __init__(self, db_info):
        self.db_info = db_info

    def connect(self):
        self.con = MySQLdb.connect(self.db_info['host'],
                                   self.db_info['username'],
                                   self.db_info['password'],
                                   self.db_info['database'])

    def cursor(self):
        self.connect()
        return self.con.cursor()

    def commit(self):
        self.con.commit()

    def close(self):
        if self.con:
            self.con.close()
