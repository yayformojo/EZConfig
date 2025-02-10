
class EZConfig():
    def __init__(self, dbname, db_path=None):
        self.dbname = dbname    
        self.setup_cursor(self.dbname)
    
    def setup_cursor(self, dbname):
        import sqlite3
        self.dbname = dbname
        self.conn = sqlite3.Connection(self.dbname)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS config(
            key TEXT PRIMARY KEY,
            value TEXT,
            modified TIMESTAMP DEFAULT current_timestamp)""")
        self.cursor.execute("""CREATE TRIGGER IF NOT EXISTS timestamp_update AFTER UPDATE ON config FOR EACH ROW BEGIN 
                            UPDATE config SET modified=current_timestamp WHERE rowid=OLD.rowid;end;""")
        self.conn.commit()
        
    def write(self, key, value):
        self.key = key
        self.value = value
        self.cursor.execute("""INSERT OR REPLACE INTO config(key, value) VALUES(?,?);""",(self.key, self.value))
        self.conn.commit()
    
    def get_config_file(self):
        return self.dbname
    
    def read(self, key, value_if_null=None):
        self.key = key
        self.value_if_null = value_if_null
        ret_key = self.cursor.execute("SELECT value FROM config WHERE key=?",(self.key,)).fetchone()
        if ret_key:
            return ret_key[0]
        else:
            if self.value_if_null == 'error':
                raise KeyError(f'Key {self.key} not found')
            return self.value_if_null
    
    def read_all(self, output=None):
        results = self.cursor.execute("SELECT key, value, modified FROM config ORDER BY key;").fetchall()
        if output == 'p':
            print(f'Config in {self.get_config_file()}:')
            for line in results:
                print(line)
        else:
            return {row[0]: row[1] for row in results}
    
    def delete(self, key, delete_level='row'): 
        """If delete_level is value_only, then only the value will be set to Null, and the key
        will not be deleted.  By default, the entire row will be deleted."""
        self.key = key
        self.delete_level = delete_level
        if self.delete_level == 'value_only':
            self.cursor.execute("UPDATE config SET value=Null WHERE key=?",(self.key,))
        elif delete_level == 'row':
            self.cursor.execute("DELETE FROM config WHERE key=?",(self.key,))
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()
    
    
if __name__ == '__main__':
    print(r"""
                  ___                __  _        
      ___  ____  / __\ ___   _ __   / _|(_)  __ _ 
     / _ \|_  / / /   / _ \ | '_ \ | |_ | | / _` |
    |  __/ / / / /___| (_) || | | ||  _|| || (_| |
     \___|/___|\____/ \___/ |_| |_||_|  |_| \__, |
                                            |___/ 
    Lightweight Script Configuration Management
     * Simple, clean syntax
     * Can read config by key or all at once
     * Config is stored in a SQLite Database, which can be queried with SQL
     * Methods:  write(), read(), read_all(), delete(), get_config_file()
     
     Using ezConfig
     ==============
     (1) Create a config instance:
        myconfig = ezConfig('config_database_file_name_here.db')
     
     (2) Write key-value pairs to the config database:
        myconfig.write('mykey', 'myvalue')
        myconfig.write('another_key', 'another_value')
     
     (3) Fetch a value and assign to a variable:
        my_config_value = myconfig.read('mykey')
        my_other_config_value = myconfig.read('another_key')
     
     (4) Delete a value:
        myconfig.delete('mykey')
     
     If you want to load the whole config at once, as a dict
     =======================================================
     cfg_info = myconfig.read_all()
 
     * See README.md file for full usage details. 
    """)
    