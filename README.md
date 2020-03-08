# schematable

a Python utility library for working with SQL tables

# Install

```
pip install schematable
```

# Basic usage

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
  db_url='postgres://user:password@localhost:5432/foo,
  schema='bar',
  table='schedule'
)

```