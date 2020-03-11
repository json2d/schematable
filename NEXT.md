## Extended database urls 

So here's an idea 💡: how about if we append the schema and table to the end of a standard db url?

```py
import schematable as st

schdl = st.SchemaTable('postgres://user:password@localhost:5432/foo#bar.schedule')

```

Specifically, we'd like a parseable url where only the `table` portion is required and the rest (`schema` and `db_url`) are optional with defaults to match our `SchemaTable` constructor spec:

```py
SchemaTable('schedule')
SchemaTable('bar.schedule')
SchemaTable('postgres://user:password@localhost:5432/foo#schedule')
SchemaTable('postgres://user:password@localhost:5432/foo#bar.schedule')

```

### The right delimiter

There's a decision to be made on which character we should use to separate the `db_url` portion from the `schema` and `table` portion. `#` appears to be the best candidate since:

- its a special character
- its not a charater used in the `db_url` spec
- its similarly used in web urls as a *fragment identifier* (eg. https://foo.io#bar.schedule) and as such it invokes a similar pattern of usage making it familiar and easier to grok for new users
