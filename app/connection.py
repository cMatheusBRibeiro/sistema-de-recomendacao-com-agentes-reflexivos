import mariadb
import sys

class Connection:
    def __init__(self):
        try: 
            conn = mariadb.connect(
                user="root",
                password="senha",
                host="localhost",
                port=3306,
                database="sistemarecomendacao"
            )
            conn.autocommit = True

            self.cur = conn.cursor()
        except mariadb.Error as e:
            print(f"Error conecting to MariaDB platform: {e}")
            sys.exit(1)
    
    def getCur(self):
        return self.cur