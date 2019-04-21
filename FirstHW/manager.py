from FirstHW.fields import *
from FirstHW.query_set import *


class Manage:
    def __init__(self):
        self.model_cls = None

    def __get__(self, instance, owner):
        if self.model_cls is None:
            self.model_cls = owner
        return self

    def create(self, **kw):
        conn = self.model_cls._conn
        cursor = conn.cursor()
        command = f'INSERT INTO {self.model_cls._table_name}('
        for k, v in kw.items():
            if isinstance(self.model_cls._fields[k], Field):
                command += k + ', '

        command = command[:-2] + ') VALUES ('

        for k, v in kw.items():
            if isinstance(self.model_cls._fields[k], Field):
                command += '?, '
        command = command[:-2] + ')'
        cursor.execute(command, [v for k, v in kw.items()
                                 if isinstance(self.model_cls._fields[k], Field)])

        conn.commit()

    def all(self):
        conn = self.model_cls._conn
        cursor = conn.cursor()
        command = f'select * from  {self.model_cls._table_name}'
        res = cursor.execute(command)
        return [self.model_cls(**item) for item in res]

    def filter(self, **kwargs):
        return QuerySet(self.model_cls, **kwargs)
