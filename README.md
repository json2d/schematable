[![PyPI version](https://badge.fury.io/py/schematable.svg)](https://badge.fury.io/py/schematable)
[![Build Status](https://travis-ci.com/json2d/schematable.svg?branch=master)](https://travis-ci.com/json2d/schematable) 
[![Coverage Status](https://coveralls.io/repos/github/json2d/schematable/badge.svg?branch=master)](https://coveralls.io/github/json2d/schematable?branch=master)

# schematable

a Python utility library for working with SQL tables

## Install

```
pip install schematable
```

## Basic usage

Go from zero to SQL query in seconds with near-zero boilerplate:

```py
import schematable as st

schdl = st.SchemaTable('schedule') # at minimum it needs a table name 

print(schdl.db_url) # sqlite:///:memory:
print(schdl.engine) # <class 'sqlalchemy.engine.base.Engine'>

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

insert_records_stmt = '''
  INSERT INTO schedule (start_time, end_time, event_name, id) VALUES ('1583531261000', '1583534865000', 'walk the doggy 🐶', 1);
'''

insert_records_stmt_2 = '''
  INSERT INTO schedule (start_time, end_time, event_name, id) VALUES ('1583708400000', '1583632800000', 'take a nap 😴', 2);
'''

schdl.engine.execute(insert_records_stmt)
schdl.engine.execute(insert_records_stmt_2)

rows = schdl.engine.execute('select event_name from schedule').fetchall()

print(rows) # ['walk the doggy 🐶', 'take a nap 😴']

```

## More advanced usage

With `sqlalchemy` under the hood you can connect to tables from all types of SQL databases:

```py
import schematable as st

schdl = st.SchemaTable(
  db_url='postgres://user:password@localhost:5432/foo',
  schema='bar',
  table='schedule'
)

```

`schematable` also integrates with `pandas` workflows like a charm, reducing the noise and friction involved with managing the arguments for their SQL related functions:

```py
import pandas as pd
import datetime

df = pd.read_sql_table(schdl.table, schdl.engine, schld.schema) # neat - everything's in one place

df['event_name']
df['start_time'] > datetime.datetime.now()
df['extracted_time'] = datetime.datetime.now()
```

## Cross database workflow

Working with multiple databases at the same time should be dead simple.

Eg. Lets say we wanted to create a new local test database on-the-fly with some data queried from our production database.

Here's the `schematable` + `pandas` way:

```py
import schematable as st
import pandas as pd

# extract dataset from production db

schdl = st.SchemaTable(
  db_url='postgres://user:password@localhost:5432/foo',
  schema='bar',
  table='schedule'
)

# select everything from 2019

select_dataset_query = '''
  select * from {schema_table} 
  where start_date between date('{from_date}') and date('{to_date}')
'''.format(
  schema_table=schdl.st, 
  from_date='2019-01-01',
  to_date='2019-12-31'
)

df = pd.read_sql(select_dataset_query, schdl.table, schdl.engine)

# load dataset into (new) test db

test_schdl = st.SchemaTable(
  db_url='sqlite:///db/test-2019.sqlite',
  table='schedule'
)

df.to_sql(test_schdl.table, test_schdl.engine, if_exists='replace', index=false)

```

## Extended URLs

Take a standard db URL and append a schema and table to the end - you get what we call a  **schematable URL**, which can be parsed into a `SchemaTable` instance:

```py
from schematable import SchemaTable

schdl = SchemaTable.parse('postgres://user:password@localhost:5432/foo#bar.schedule')

print(schdl.db_url) # postgres://user:password@localhost:5432/foo
print(schdl.schema) # bar
print(schdl.table) # schedule

```

They're primarily handy for usecases involving serialization and deserialization of schematables:

```env
# staging.env
SCHEDULE_SCHEMATABLE_URL=sqlite:///staging.db#bar.schedule
```

```py
schdl = SchemaTable.parse(os.environ['SCHEDULE_SCHEMATABLE_URL'])

print(schdl.db_url) # sqlite:///staging.db
print(schdl.schema) # bar
print(schdl.table) # schedule
```

More specifically, schematable URLs are composed of a `db_url`, `table`, and `schema` component where (just like the `SchemaTable` constructor) only the `table` component is required:

```py
SchemaTable.parse('schedule')
SchemaTable.parse('bar.schedule')
SchemaTable.parse('sqlite:///staging.db#schedule')
SchemaTable.parse('postgres://user:password@localhost:5432/foo#bar.schedule')
```

## Boilerplate reduction

Here are before-and-after snippets showing some code you won't have to write anymore using `schematable` to do your SQL things:

Eg. Here's checking if a table exists:

#### before
```py
import sqlalchemy as sa

schdl_db_url = 'sqlite://'
schdl_table = 'schedule'
schdl_engine = sa.create_engine(schdl_db_url)
if schdl_engine.has_table(schdl_table):
  # do the thing
```

#### after
```py
import schematable as st

schl = st.parse('schedule')
if schdl.engine.has_table(schdl.table, schdl.schema):
  # do the thing
```

#### after next
```py
import schematable as st

schl = st.parse('schedule')
if schdl.exists():
  # do the thing
```

