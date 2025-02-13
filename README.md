# EZConfig
**Quick and easy to add**
**Key-Value store for your Configuration or State, in a lightweight, portable SQLite database file**

 - EZConfig uses compact, intuitive syntax.
 - The source code should be readable and easy to follow: It was written with simplicity in mind over comprehensive features.
 - You can use it in place of modules like Configparser, or manually keeping information in YAML/text files.
 - Extend it for your own use, or import it as a small library whenever you need to store State or Configuration (or both).
 - You can query the database file with SQL: no parsing files in various formats.
 - Keys can be read individually and assigned to variables, or they can be read all-at-once as a dictionary.  

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
<br>

### Read a config item
```python
server = mycfg.read('server_name') # assigns 'localhost' to the variable
port = mycfg.read('port_number', value_if_null='error') # Returns an exception if the key is missing or the value is null.
update_interval = mycfg.read('update_interval',60) # Returns 60 as a default interval if none exists
```
_This returns the value of the key specified. By default a Null key will return **None**._<br>
<br>

### Read the entire config into a dictionary
```python
mycfg_dict = {}
mycfg_dict = mycfg.readall()
```
<br>

### Print the entire config, including modified timestamps
```python
mycfg.readall('p') 
```
<br>

### Delete a config item: entire key-value pair, or only value
```python
mycfg.delete('server_name', 'value_only') # deletes _only_ the value 'localhost' and sets the value of the key 'server_name' to Null
mycfg.delete('mykey') # deletes the entire key, removing the row from the database entirely
```
<br>

### dbname property
If you need the name of the database file, the property 'dbname' can be used
```python
mydb = mycfg.dbname
```
<br>

## Methods in the EZConfig class:

| Method                |
|-----------------------|
| write(key, value)     |
| read(key, value_if_null=None)      |
| read_all(output=None)  |
|delete(key, delete_level='row')|
<br>

## Timestamps & accessing the database file:
A column in the database called `modified` is stored in the database when the key-value pair is created, and updated each time the key is updated.

The database is only one table.  You can use the SQLite client tool `sqlite3` to use SQL directly on the database.
```sql
SELECT * FROM config;

SELECT * FROM sqlite_master; # Shows the schema, including the trigger to update the 'modified' timestamp.
```

