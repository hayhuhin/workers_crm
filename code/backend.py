import mysql.connector
from settings import USERNAME, PASSWORD



class database_session(object):
    """ class that connecting to the database and sending the queries that it gets from the init arguments """
    def __init__(self, args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.config = {
            'user': USERNAME,
            'password': PASSWORD,
            'host': 'localhost',
            'database': 'workers',
            'raise_on_warnings': True
        }
        self.cnx = mysql.connector.connect(**self.config)
        self.cursor = self.cnx.cursor()


    def update(self,table,set_data,argument,prev_arg):
        """ update method that sends 'update set...' query and then commits """
        query = f"update {table} set {set_data}='{argument}' where name='{prev_arg}'; "
        self.cursor.execute(query)
        self.cnx.commit()


    def delete(self,table,set_data,prev_arg):
        query = f"delete from {table} where {set_data}='{prev_arg}'; "
        self.cursor.execute(query)
        self.cnx.commit()


    def create_rows(self,table_name,**kwargs):
        self.table_name = table_name
        self.kwargs = kwargs
        key_inserts = ''
        value_inserts = ''
        query = f"insert into {self.table_name} "
        # print(self.kwargs['kwargs'].keys())

        for key in self.kwargs['kwargs']:
            # print(key)
            key_inserts += f"{key},"
            value_inserts += f"'{self.kwargs['kwargs'][key]}',"
        key_inserts = key_inserts[:-1]
        value_inserts = value_inserts[:-1]

        query += "(" + key_inserts + ")" + " values " + "(" + value_inserts + ")" + ";"
        print(query)
        self.cursor.execute(query)
        self.cnx.commit()


    def execute_commands(self,command):
        """ execute sql command : write the command argument as a string of the sql command 
        example: 'select * from TABLE_NAME; ' """
        
        self.cursor.execute(command)
        for lines in self.cursor:
            print(lines)


    def create_table(self,table_name,**kwargs):

        self.kwargs = kwargs

        self.query = f"create table {table_name} ("

        for key in self.kwargs['kwargs']:
            self.query += f"{key} {self.kwargs['kwargs'][key]},"


        if self.query[-1] == ',':
            self.query = self.query[:-1]


        self.query += ');'
        self.cursor.execute(self.query)


    def close_session(self):
        """closing the connection to the DB session"""
        self.cnx.close()



#running as a source script 
if '__main__' == __name__:

    data1 = ['desc position;', 'select * from rank_;']
    conn = database_session(data1)
    conn.execute_commands('select * from worker;')
    conn.close_session()
