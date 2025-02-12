"""
Test the EZConfig Class
"""

from ezconfig import EZConfig 
import pytest 
import sqlite3

def open_test_conn(dbname):
    testcfg = EZConfig(dbname)
    return testcfg

testcfg = open_test_conn(':memory:')

# __init__() method TEST
def test_database_connection():
    assert isinstance(testcfg, EZConfig)
    
def test_invalid_sqlite_file_fails():
    with pytest.raises(sqlite3.DatabaseError):
        _ = EZConfig('./tests/invalid_sqlite_file_that_exists.db')

# read() *empty* method TEST    
def test_read_all_empty():
    results = {}
    results = testcfg.read_all()
    assert results == {}   

# read_all *empty* method TEST
def test_read_all_empty_print_option(capsys):
    testcfg.read_all('p')
    captured = capsys.readouterr()
    assert captured.out == 'Config in :memory::\n'
    assert captured.err == ''
    
# write() method TEST
def test_write_none_key_raises(): 
    with pytest.raises(ValueError):
        testcfg.write(None,'value')

def test_write_empty_string_raises():
    with pytest.raises(ValueError):
        testcfg.write('', 'value')

def test_write_binary_key_raises():
    with pytest.raises(ValueError):
        testcfg.write(b'0x0020','value')

def test_write_standard_key_return():
    result = testcfg.write('justwritekey','justwriteval')
    assert result is None
    
def test_write_key_and_read_it():
    testcfg.write('normalkey','normalval')
    result = testcfg.read('normalkey')
    assert result == 'normalval'

def test_write_key_and_read_it_int_returns_string():
    """ This is a database artifact; value column is type TEXT"""
    testcfg.write('normalkey',-10)
    result = testcfg.read('normalkey')
    assert result == '-10'

def test_write_key_and_read_it_bool_returns_str():
    """ This is a SQLite artifact"""
    testcfg.write('normalkey',True)
    result = testcfg.read('normalkey')
    assert result == '1'

def test_write_key_and_read_it_bool_str_returns_str():
    testcfg.write('normalkey','False')
    result = testcfg.read('normalkey')
    assert result == 'False'

def test_write_key_and_read_it_blank():
    testcfg.write('normalkey','')
    result = testcfg.read('normalkey')
    assert result == ''
    
# properties TEST
def test_property_dbname():
    assert testcfg.dbname == ':memory:'

# read() method TEST
def test_read_base():
    testcfg.write('readbasekey','readbaseval')
    result = testcfg.read('readbasekey')
    assert result == 'readbaseval'

def test_read_valuenull_error():
    with pytest.raises(KeyError) as testex:
        testcfg.read('readnullkey','error')
    assert str(testex.value) == "'Key readnullkey not found'"
    
def test_read_valuenull_none():
    result = testcfg.read('readnullkey')
    assert result is None

def test_read_valuenull_other():
    result = testcfg.read('readnullkey','')
    assert result == ''

# read_all() method TEST
def test_read_all_print(capsys):
    testcfg.read_all('p')
    captured = capsys.readouterr()
    assert captured.out is not None
    assert captured.err == ''
    
def test_read_all_is_dict():
    object = testcfg.read_all()
    assert isinstance(object, dict)

# delete() method TEST
def test_delete_base():
    testcfg.write('deletemekey','deletemeval')
    testcfg.delete('deletemekey')
    result = testcfg.read('deletemekey')
    assert result is None
    
def test_delete_row():
    testcfg.write('deletemekey','deletemeval')
    testcfg.delete('deletemekey','row')
    result = testcfg.read('deletemekey')
    assert result is None

def test_delete_value_only():
    testcfg.write('delkey','delval')
    testcfg.delete('delkey','value_only')
    
    keyresult = testcfg.cursor.execute("SELECT key FROM config WHERE key='delkey';").fetchall()
    results = keyresult[0]
    assert results == ('delkey',)
    
    valresult = testcfg.cursor.execute("SELECT value FROM config where key='delkey';").fetchall()
    results_val = valresult[0]
    assert results_val == (None,) # None, not a string "None"
    
def test_delete_anyother():
    testcfg.write('deletemekey','some_incorrect_val')
    with pytest.raises(ValueError):
        testcfg.delete('deletemekey','teststring')
    

# __del__() method TEST
# @pytest.mark.skip
def test_conn_close():
    # import sqlite3
    testcfg.__del__()
    # testcfg.conn.close()
    with pytest.raises(sqlite3.ProgrammingError) as testex:
        testcfg.cursor.execute("analyze;")
    assert testex


# def test_del_method():
#     import gc
#     import weakref
    
#     temp_cfg = EZConfig(':memory:')
#     conn_ref = weakref.ref(temp_cfg.conn)
#     del temp_cfg
#     gc.collect()
#     assert conn_ref() is None or conn_ref().total_changes == -1

