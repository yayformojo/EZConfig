# EZConfig
### Simple application configuration management module, using SQLite.

Intended to be as concise as possible in code.<br>
Supports an easy, key-value store which allows loading the config in its entirety (as a python dict), or by section or individual key. 

The config values can be read all-at-once, or individually.  

### Methods in the EZConfig class.

| Method                |Comment |
|-----------------------|---|
| write(key, value)     | |
| read(key, value)      | |
| read_all(output=None)  | Argument is optional.<br>Reads all config values at once, storing them in a dictionary.<br>Use output='p' to print the config (used in debugging mostly). |
|delete(key, delete_level='row')| Argument is optional.  Use delete_level='value_only'<br>to delete the value, setting<br> it to Null, but leaving the key. |


When `read_all(output='p')` is used, the output will include the modified timestamp.  This timestamp is stored in the database when the key-value pair is created, and updated each time the key is updated.

The database is only one table.  You can use the SQLite client tool `sqlite3` to use SQL directly on the database.
