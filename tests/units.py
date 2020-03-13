import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

# import logging
# logger = logging.getLogger(__name__)

import attr

import unittest

from schematable import SchemaTable

class TestEverything(unittest.TestCase):

  def test_least_resistance(self):
    schdl = SchemaTable('schedule')

    self.assertIn(schdl.db_url, ('sqlite://', 'sqlite:///:memory:'))
    self.assertEqual(schdl.schema, None)
    self.assertEqual(schdl.table, 'schedule')
    self.assertEqual(schdl.stab, 'schedule')


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
      INSERT INTO schedule (start_time, end_time, event_name, id) VALUES ('1583531261000', '1583534865000', 'walk the doggy 🐶', 1);
    '''
    insert_records_stmt_2 = '''
      INSERT INTO schedule (start_time, end_time, event_name, id) VALUES ('1583708400000', '1583632800000', 'take a nap 😴', 2);
    '''

    schdl.engine.execute(insert_records_stmt)
    schdl.engine.execute(insert_records_stmt_2)

    res = schdl.engine.execute('select * from schedule')
    rows = list(res)

    self.assertEqual(rows[0]['event_name'], 'walk the doggy 🐶')
    self.assertEqual(len(rows), 2)

  def test_alias(self):
    schdl = SchemaTable('schedule')

    self.assertEqual(schdl.schema_table, 'schedule')
    self.assertEqual(schdl.stab, 'schedule')
    self.assertEqual(schdl.st, 'schedule')

    schdl_temp = SchemaTable(schema='temp', table='schedule')

    self.assertEqual(schdl_temp.schema_table, 'temp.schedule')
    self.assertEqual(schdl_temp.stab, 'temp.schedule')
    self.assertEqual(schdl_temp.st, 'temp.schedule')


  def test_immutable(self):
    schdl = SchemaTable(schema='main', table='schedule')
  
    with self.assertRaises(attr.exceptions.FrozenInstanceError):
      schdl.table = 'comments'
      schdl.schema = 'temp'
      schdl.db_url = 'sqlite:///db/test.sqlite'

    schdl_temp = attr.evolve(schdl, schema = 'temp')

    self.assertEqual(schdl_temp.schema, 'temp')

  def test_table_validation(self):

    invalid_tables = [
      None,
      42,
      'schedules!',
      'schedules...',
      'sqlite:///db/test.sqlite',
      '!@#$%^&*()+={}[]\|;:\'",<.>/?'
    ]

    for table in invalid_tables:
      with self.assertRaises(Exception):
        SchemaTable(table)

  def test_ext_url(self):

    valid_urls = [
      'main.schedule',
      '#main.schedule',
      'schedule',
      '#schedule',
      'sqlite:///db/test.sqlite#schedule',
      'sqlite:///db/test.sqlite#main.schedule',
    ]

    try:
      for url in valid_urls:
        schdl = SchemaTable.parse(url)
        self.assertEqual(schdl.table, 'schedule')
    except:
      self.fail('validation should have passed but exception was raised')


    invalid_urls = [
      'main',
      'main.',
      'sqlite:///db/test.sqlite',
    ]

    for url in invalid_urls:
      with self.assertRaises(Exception):
        SchemaTable.parse(url)


    schdl = SchemaTable.parse('schedule')

    self.assertIn(schdl.url, ('sqlite://#schedule', 'sqlite:///:memory:#schedule'))
    self.assertIn(schdl.db_url, ('sqlite://', 'sqlite:///:memory:'))
    self.assertEqual(schdl.schema, None)
    self.assertEqual(schdl.table, 'schedule')
    self.assertEqual(schdl.schema_table, 'schedule')

    schdl = SchemaTable.parse('main.schedule')

    self.assertIn(schdl.url, ('sqlite://#main.schedule', 'sqlite:///:memory:#main.schedule'))
    self.assertIn(schdl.db_url, ('sqlite://', 'sqlite:///:memory:'))
    self.assertEqual(schdl.schema, 'main')
    self.assertEqual(schdl.table, 'schedule')
    self.assertEqual(schdl.schema_table, 'main.schedule')
        

unittest.main()