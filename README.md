# EZConfig
### Simple application configuration management module, using SQLite.

Intended to be as concise as possible in code.  Supports an easy, key-value store which allows loading the config in its entirety (as a python dict), or by section or individual key. 

The config values can be read all-at-once, or individually.  

### Methods in the EZConfig class.

| Method                |Comment |
|-----------------------|---|
| write(key, value)     | |
| read(key, value)      | |
|read_all(output=None)  | Argument is optional.  Use output='p' to print,<br>used in debugging mostly. |
|delete(key, delete_level='row'| Use delete_level='value_only'<br>to delete the value, setting<br> it to Null, but leaving the key. |

