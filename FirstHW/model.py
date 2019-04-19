import sqlite3
from FirstHW.manager import *
from FirstHW.fields import *


class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        if name == 'Model':
            return super().__new__(mcs, name, bases, namespace)

        meta = namespace.get('Meta')
        if meta is None:
            raise ValueError('meta is none')
        if not hasattr(meta, 'table_name'):
            raise ValueError('table_name is empty')

        fields = {}
        for base in bases:
            fields.update(base._fields)

        fields.update({k: v for k, v in namespace.items() if isinstance(v, Field)})
        namespace['_fields'] = fields
        namespace['_table_name'] = meta.table_name

        conn = sqlite3.connect("newDB.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()
        # Создание таблицы
        command = f"create table if not exists {meta.table_name}("
        for k, v in fields.items():
            if isinstance(v, StringField):
                command += f'{k} text'
            elif isinstance(v, IntField):
                command += f'{k} integer '
            if v.required:
                command += 'not null'
            if v.default is not None:
                command += f'default=\'{v.default}\','
            command += ', '
        command += 'raw_id integer PRIMARY KEY)'

        cursor.execute(command.lower())

        conn.row_factory = sqlite3.Row
        namespace['_conn'] = conn

        return super().__new__(mcs, name, bases, namespace)


class Model(metaclass=ModelMeta):
    _fields = {}
    _table_name = ''
    _conn = None

    class Meta:
        table_name = ''

    objects = Manage()

    # todo DoesNotExist
    # DoesNotExist = DoesNotExistDescrt('1')

    def __init__(self, *_, **kwargs):
        for field_name, field in kwargs.items():
            value = getattr(self, field_name).validate(field)
            setattr(self, field_name, value)
        if 'raw_id' in kwargs.keys():
            self.raw_id = kwargs['raw_id']
        else:
            self.raw_id = None

    def save(self):
        conn = self._conn
        cursor = conn.cursor()
        if self.raw_id is None:

            command = f'INSERT INTO {self._table_name}('
            for k, v in self._fields.items():
                if isinstance(v, Field):
                    command += k + ', '

            command = command[:-2] + ') VALUES ('

            for k, v in self._fields.items():
                if isinstance(v, Field):
                    command += '\'' + str(getattr(self, k) if not None else 'Null') + '\', '
            command = command[:-2]
            command += ')'
        else:
            command = f' UPDATE {self._table_name} SET '
            for k in self._fields.keys():
                command += k + ' = \'' + str(getattr(self, k)) + '\', '
            command = command[:-2] + ' where raw_id = \'' + str(self.raw_id) + '\''
        res = cursor.execute(command)
        if self.raw_id is None:
            self.raw_id = res.lastrowid
        conn.commit()

    def delete(self):
        if self.raw_id is None:
            del self
        else:
            conn = self._conn
            cursor = conn.cursor()
            command = f"DELETE FROM {self._table_name} WHERE raw_id = {self.raw_id}"
            cursor.execute(command)
            conn.commit()
