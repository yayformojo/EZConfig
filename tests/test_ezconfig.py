"""
Test the EZConfig Class
"""

from ezconfig import EZConfig 
import pytest 


def open_test_conn(dbname):
    testcfg = EZConfig(dbname)
    return testcfg

testcfg = open_test_conn(':memory:')

def test_conn():
    assert isinstance(testcfg, EZConfig)
    
def test_read_all_empty():
    results = {}
    results = testcfg.read_all()
    assert results == {}   

def test_read_all_empty_print(capsys):
    testcfg.read_all('p')
    captured = capsys.readouterr()
    assert captured.out == 'Config in :memory::\n'
    assert captured.err == ''
    
        
def test_write_none_key(): # <-- fix EZConfig; this should error ***********
    testcfg.write(None,'value')
    assert testcfg.read(None) is None

def test_write():
    result = testcfg.write('justwritekey','justwriteval')
    assert result is None
    
def test_write_normal_key():
    testcfg.write('normalkey','normalval')
    result = testcfg.read('normalkey')
    assert result == 'normalval'


def test_property_dbname():
    assert testcfg.dbname == ':memory:'


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

def test_read_all_print(capsys):
    testcfg.read_all('p')
    captured = capsys.readouterr()
    assert captured.out is not None
    assert captured.err == ''


def test_delete_base():
    testcfg.write('deletemekey','deletemeval')
    testcfg.delete('deletemekey')
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
    

    
# @pytest.mark.skip
def test_conn_close():
    import sqlite3
    testcfg.conn.close()
    with pytest.raises(sqlite3.ProgrammingError) as testex:
        testcfg.cursor.execute("analyze;")
    assert testex






