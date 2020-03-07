import attr
import sqlalchemy as sa

@attr.s(frozen=True)
class SchemaTable(object):
  table: str = attr.ib()
  schema = attr.ib(default=None, validator=attr.validators.instance_of((str, type(None))))
  stab: str = attr.ib()
  st: str = attr.ib()
  db_url: str = attr.ib(default='sqlite:///:memory:') # in-memory db
  engine: sa.engine.base.Engine = attr.ib()

  @db_url.validator
  def check_url(self, attribute, value):
    pass

  @stab.default
  def stab_default(self):
    return self.schema + '.' + self.table

  @st.default # alias of stab
  def st_default(self):
    return self.stab

  @engine.default
  def engine_default(self):
    return sa.create_engine(self.db_url)

  def todict(self):
    return attr.asdict(self) # TODO: exclude engine attr

