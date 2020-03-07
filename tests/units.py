import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

# import logging
# logger = logging.getLogger(__name__)

import attr

import unittest

from schematable import SchemaTable

class TestEverything(unittest.TestCase):

  def test_base(self):

    schdl = SchemaTable(schema='main', table='schedule')
    # schdl = SchemaTable(schema='main', table='schedule', db_url='sqlite:///db/test.sqlite') # use local sqlite file

    self.assertIn(schdl.db_url, ('sqlite://', 'sqlite:///:memory:'))
    self.assertEqual(schdl.schema, 'main')
    self.assertEqual(schdl.table, 'schedule')
    self.assertEqual(schdl.stab, 'main.schedule')
    self.assertEqual(schdl.st, 'main.schedule')

    create_table_stmt = '''
      create table schedule
      (
        start_time timestamp,
        end_time timestamp,
        event_name text,
        id int not null
          constraint schedule_pk
            primary key
      );
    '''

    schdl.engine.execute(create_table_stmt)

    self.assertTrue(schdl.engine.dialect.has_table(schdl.engine, 'schedule'))

    insert_records_stmt = '''
      INSERT INTO schedule (start_time, end_time, event_name, id) VALUES ('1583531261000', '1583534865000', 'walk dog', 1);
    '''
    insert_records_stmt_2 = '''
      INSERT INTO schedule (start_time, end_time, event_name, id) VALUES ('1583708400000', '1583632800000', 'take a nap 😴', 2);
    '''

    schdl.engine.execute(insert_records_stmt)
    schdl.engine.execute(insert_records_stmt_2)

    res = schdl.engine.execute('select * from schedule')
    rows = list(res)

    self.assertEqual(rows[0]['event_name'], 'walk dog')
    self.assertEqual(len(rows), 2)

    
  def test_immutable(self):
    schdl = SchemaTable(schema='main', table='schedule')
  
    with self.assertRaises(attr.exceptions.FrozenInstanceError):
      schdl.table = 'comments'
      schdl.schema = 'temp'
      schdl.db_url = 'sqlite:///db/test.sqlite'

    schdl_temp = attr.evolve(schdl, schema = 'temp')

    self.assertEqual(schdl_temp.schema, 'temp')
    


unittest.main()