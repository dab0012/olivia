class QueryBuilder:

    def __init__(self, db_driver):

        self.db_driver = db_driver
        self.querys = {

            # Querys for MySQL
            'mysql': {

                'insert': {
                    'packages': 'INSERT INTO packages (name, description, version, publication_date, requires_compilation, in_cran, in_bioconductor, mantainer, author_data, license) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    'dependencies': 'INSERT INTO dependencies (name, version, type) VALUES (%s, %s, %s)',
                    'package_dependency': 'INSERT INTO package_dependency (package_id, dependency_id) VALUES (%s, %s)'
                },
                'exists': {
                    'packages': 'SELECT * FROM packages WHERE name = %s',
                    'dependencies': 'SELECT * FROM dependencies WHERE name = %s AND version = %s AND type = %s',
                    'link': 'SELECT * FROM links WHERE package_id = %s'
                },
                'select': {
                    'packages': 'SELECT * FROM packages WHERE name = %s',
                    'package_dependency' : 'SELECT * FROM package_dependency WHERE package_id = %s',
                    'dependencies': 'SELECT * FROM dependencies WHERE id = %s',
                    'links': 'SELECT * FROM links WHERE package_id = %s',
                    'package_link': 'SELECT * FROM package_link WHERE package_id = %s'
                }
            },

            # Querys for SQLite
            'sqlite': {
                'insert': {},
                'exists': {},
            }
        }

    def get_query(self, query_type, query_name):
        '''
        Returns the query for the given query type and query name

        Parameters
        ----------
        query_type : str
            The type of the query. It can be 'insert' or 'exists'
        query_name : str
            The name of the query. It can be 'package', 'dependency' or 'link'

        Returns
        -------
        str
            The query
        '''

        return self.querys[self.db_driver][query_type][query_name]
