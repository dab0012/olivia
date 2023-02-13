# Author: Daniel Alonso Báscones
# Date: 2022-12-23
# Project: TFG OLIVIA

from colorama import Fore, Style

import mysql.connector
from modules.database.db_handler import DatabaseHandler
from modules.database.query_builder import QueryBuilder


class MySQLHandler(DatabaseHandler):
    '''
    Class for connecting to mysql database
    
    '''
    
    def __init__(self, cnf):
        '''
        Method to initialize the class
        '''
        self.cnf = cnf
        self.cnx = None
        
    def get_connection(self):
        '''
        Method to get the connection to the database
        '''

        # Return the connection to the database
        return self.cnx

    def open_connection(self):
        '''
        Method to open the connection to the database
        '''

        # Open the connection to the database
        try:

            self.cnx = mysql.connector.connect(
                user=self.cnf['user'],
                password=self.cnf['password'],
                host=self.cnf['host'],
                database=self.cnf['database']
            )
        
        except Exception as e:
                
            print(Fore.RED)
            print("Exception in class MySqlHandler, method open_connection")
            print("Error: The database connection could not be established")
            print("Error: ", e)
            print(Style.RESET_ALL)
            exit(1)

    def close_connection(self):
        '''
        Method to close the connection to the database
        '''

        # Close the connection to the database
        self.cnx.close()    

    def execute_query(self, query: str, params: tuple = None) -> list[tuple]:
        '''
        Method to execute a query in the database

        Parameters:
        -----------
            query (str): Query to be executed
            params (tuple): Parameters of the query

        Returns:
        --------
            list[tuple]: List of tuples with the result of the query
        '''


        # Create a cursor to execute the query
        cursor = self.cnx.cursor()

        # Execute the query
        cursor.execute(query, params)

        # Get the result of the query
        result = cursor.fetchall()

        # Close the cursor
        cursor.close()

        # Return the result of the query
        return result

    def get_QueryBuilder(self):
        return QueryBuilder('mysql')