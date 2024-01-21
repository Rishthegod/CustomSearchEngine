#store previous queries and search history in order to no exhaust API limit and lay the foundation for machine learning
import sqlite3
import pandas as pd

class DBStorage():
    def __init__(self):
        self.con = sqlite3.connect('links.db')
        self.setup_tables() #run setup tables on init
    def setup_tables(self):
        cur = self.con.cursor() #essentially a socket connection to connect to database
        '''Create the following table in our database if it does not exist that has all the following 
        fields and their specified data types, relevance field can be used in machine learning 
        applications in the future. each query link combo must be unique'''
        results_table = r"""
        CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY,
        query TEXT,
        rank INTEGER,
        link TEXT,
        title TEXT,
        snippet TEXT,
        html TEXT,
        created DATETIME,
        relevance INTEGER,
        UNIQUE(query,link)
        )
        """
        cur.execute(results_table)
        self.con.commit() #commit changes (the results table) to the database
        cur.close() #close the connection like in a  socket
    def query_results(self,query):
        df = pd.read_sql(f"select * from results where query='{query}' order by rank asc;", self.con) #get all the results stored from that query and rank them in ascending order
        return df
    def insert_row(self,values):
        cur = self.con.cursor()
        try:
            cur.execute('INSERT INTO results(query,rank,link,title,snippet,html,created) VALUES(?,?,?,?,?,?,?)',values) #using question marks for Values field ensures that we do not accidently pass in malformed data into our database, so we let sqlite format it for us
            self.con.commit()
        except sqlite3.IntegrityError:
            '''sql integrity error may occur if that data already exists in the database, so we can pass over it'''
            pass
        cur.close() #close connection we opened
