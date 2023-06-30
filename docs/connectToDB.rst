ConnectToDB
===================

This library establishes infrastructure that allows the linking of Hydra with the database. 

.. code-block:: python 

    class DBManager:

    # Function to connect with db
    def __init__(self,configPath="../Hydra.cfg"):

        """Establishes connection to MySQL Database.

        Parameters
        --------------
        dbhost : str, optional
            Database host, default set to hallddb on ifarm

        dbuser : str, optional
            Database username, default set to aimon
        
        dbname : str, optional
            Name of a database to connect, default set to hydra

        Exits
        --------------
        CANNOT CONNECT TO DATABASE
            If connection to database can not be established.

        Returns
        --------------
        Curser to the mysql database.

        """
        try:
            with open(configPath) as parms_json:
                parms=json.load(parms_json)
                
                dbhost=parms["DB_CONNECTION"]["Host"]
                dbuser=parms["DB_CONNECTION"]["User"]
                dbname=parms["DB_CONNECTION"]["DB"]

        except Exception as e:
            print(e)
            exit(1)

        try:
            print(dbhost,dbuser,dbname)
            self.dbcnx=MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
            self.dbcursor=self.dbcnx.cursor(MySQLdb.cursors.DictCursor)
        except:
            print("ERROR: CANNOT CONNECT TO DATABASE")
            exit(1)

        print("CONNECTED")


    def FetchAll(self, query):
        """ Executes the query and returns all the results

        PARAMETERS
        ------------------------
        query : MySQL Query to execute

        RETURNS
        ------------------------
        Results obtained after executing the query

        """
        try:
            self.dbcursor.execute(query)
            results = self.dbcursor.fetchall()
        except Exception as e:
            print("DB Error: ", e)
            print("with query: ", query)
            logging.error("DB error with query: "+str(query))
            logging.error(e)
            print("Trying to reconnect...")
            self.dbcnx.ping(True)
            if self.dbcnx.open:
                try:
                    self.dbcursor=self.dbcnx.cursor(MySQLdb.cursors.DictCursor)
                    self.dbcursor.execute(query)
                    results = self.dbcursor.fetchall()
                    return results
                except Exception as e:
                    print("DB error after re-establishing connection:", e)
                    print("with query: ", query)
                    logging.error("DB error with query: "+str(query))
                    logging.error(e)
            else:
                print("ping failed to connect")
            return []
            
        return results

    
    def Update(self, query):
        """

        PARAMETERS
        ----------------------------
        query : MySQL Query to execute

        RETURNS
        -----------------------------
        Commits after executing the query to update the database

        """
        try:
            self.dbcursor.execute(query)
            self.dbcnx.commit()
        except:
            print("DB error with query: ", query)
            logging.error("DB error with query: "+str(query))
            print("Trying to reconnect...")
            self.dbcnx.ping(True)
            if self.dbcnx.open:
                try:
                    self.dbcursor=self.dbcnx.cursor(MySQLdb.cursors.DictCursor)
                    self.dbcursor.execute(query)
                    self.dbcnx.commit()
                except Exception as e:
                    print("DB error after re-establishing connection:", e)
                    print("with query: ", query)
                    logging.error("DB error with query: "+str(query))
                    logging.error(e)
            else:
                print("ping failed to connect")

    def Close(self):
        print("closing cursor")
        self.dbcursor.close()
        print("closing connection")
        self.dbcnx.close()
        print("closed")