import mysql.connector
from settings import USERNAME, PASSWORD


class database_session(object):
    def __init__(self, args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.query = [i for i in kwargs]
        self.config = {
            'user': USERNAME,
            'password': PASSWORD,
            'host': 'localhost',
            'database': 'workers',
            'raise_on_warnings': True
        }

        self.cnx = mysql.connector.connect(**self.config)

        self.cursor = self.cnx.cursor()

        self.printf()

    def printf(self):
        if self.args:
            for n in self.args:
                print(n)
                self.cursor.execute(n)
                for i in self.cursor:
                    print(i)

    def run(self):
        self.cnx.close()


if '__main__' == __name__:
    data1 = ['desc position;', 'select * from rank_']
    data = 'select * from rank_;'
    conn = database_session(data1)
    conn.run()
