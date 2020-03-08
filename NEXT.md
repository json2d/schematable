## Extended database urls 

So how about of we appended the schema and table at the end of a standard db url?

```py
import schematable as st

schdl = st.SchemaTable('postgres://user:password@localhost:5432/foo[bar.schedule]')

```