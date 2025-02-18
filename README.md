# EZConfig
**Quick and easy key-value store for your Configuration or State**

 - EZConfig uses compact, intuitive syntax.
 - The source code should be readable and easy to follow: It was written with simplicity in mind over comprehensive features.
 - You can use it in place of modules like Configparser, or manually keeping information in YAML/text files.
 - Extend it for your own use, or import it as a small library whenever you need to store State or Configuration (or both).
 - Keys can be read individually and assigned to variables, or they can be read all-at-once as a dictionary.
 - The database is [SQLite](https://sqlite.org).  One file per EZConfig instance.
 - Backup method saves the current snapshot as a sqlite file.

## Usage Examples

### Create the config
```python
mycfg = EZConfig('database_file_name.db')
```
_The file extension db is optional, you can use no extension (e.g. 'appconfig') or another extension such as '.sqlite'_<br>
<br>

### Write a config item
```python
mycfg.write('server_name', 'localhost')
```
The write() method also returns the value:
```python
server = mycfg.write('server_name','localhost')
# server will be 'localhost'
```

<br>

### Read a config item
```python
server = mycfg.read('server_name')
# returns the value

port = mycfg.read('port_number', value_if_null='error')
# Returns exception if the key is missing/null.

update_interval = mycfg.read('update_interval',60)
# Returns 60 as a default interval if none exists
```
_This returns the value of the key specified. By default a Null key will return **None**._<br>
<br>

### Read the entire config into a dictionary
```python
mycfg_dict = {}
mycfg_dict = mycfg.readall()
```
<br>

### _Print_ the entire config, including modified timestamps (for debugging)
```python
mycfg.readall('p') 
```
<br>

### Delete a config item: entire key-value pair, or only value
```python
mycfg.delete('server_name', 'value_only')
# deletes _only_ the value 'localhost' and sets the value of the key 'server_name' to Null

mycfg.delete('mykey')
# deletes the entire key, removing the row from the database entirely
```
<br>

### Querying the config database directly
```python
mycfg.query("SELECT key, value, comment, modified FROM config WHERE key='server';")
# returns 'server_name', 'localhost', 'comment', 'yyyy-mm-dd HH:MM:SS'
```
<br>

### Backup the entire config database file:
```python
mycfg.backup('mycfg_backup.db')
# saves the current config into a sqlite database called 'mycfg_backup.db'
```
<br>

### dbname property
If you need the name of the config database file, the property 'dbname' can be used
```python
mydb = mycfg.dbname
```
<br>

## Methods in the EZConfig class:

| Method                |Comments |
|-----------------------|---------|
| write(key, value)     | Value can be None<br>Returns the value assigned |
| read(key, value_if_null=None)      | See notes about value_if_null |
| read_all(output=None)  | This will by default return a dictionary<br>For debug, this can print to the console |
| delete(key, delete_level='row')| By default will delete the row from the database |
| query(sql_query)  | DROP is not supported and will raise an exception |
| backup(filename)  | Config can be in use; uses sqlite native backup|
<br>


## About the Database file
The database is only one table (config).  You can use the [SQLite client tool](https://sqlite.org/download.html) `sqlite3` to use SQL directly on the database:
```sql
SELECT * FROM config;

SELECT * FROM sqlite_master; # Shows the schema, including the trigger to update the 'modified' timestamp.
```
## Timestamps & accessing the database file:
A column in the database called `modified` is stored in the database when the key-value pair is created, and updated each time the key is updated.

