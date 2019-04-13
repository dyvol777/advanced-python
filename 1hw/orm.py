import sqlite3


class Field:
    def __init__(self, f_type, required=True, default=None):
        self.f_type = f_type
        self.required = required
        self.default = default

    def validate(self, value):
        if value is None and not self.required:
            return None
        # todo exceptions
        return self.f_type(value)


class IntField(Field):
    def __init__(self, required=True, default=None):
        super().__init__(int, required, default)


class StringField(Field):
    def __init__(self, required=True, default=None):
        super().__init__(str, required, default)


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

        return super().__new__(mcs, name, bases, namespace)


class QuerySet:
    def __init__(self, model_cls, **conditions):
        self.model = model_cls
        self.conditions = conditions

    def get(self):
        conn = sqlite3.connect("newDB.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        command = f'select * from {self.model._table_name} where '
        for k, v in self.conditions.items():
            command += k + ' = \'' + str(v) + '\' and '
        command = command[:-5]
        res = cursor.execute(command).fetchall()
        return [self.model(**item) for item in res]

    def filter(self, **kwargs):
        self.conditions.update(kwargs)
        return self

    def delete(self):
        conn = sqlite3.connect("newDB.db")
        cursor = conn.cursor()
        command = f'delete from {self.model._table_name} where '
        for k, v in self.conditions.items():
            command += k + ' = \'' + str(v) + '\' and '
        command = command[:-5]
        cursor.execute(command)
        conn.commit()

    def update(self):
        pass


class Manage:
    def __init__(self):
        self.model_cls = None

    def __get__(self, instance, owner):
        if self.model_cls is None:
            self.model_cls = owner
        return self

    def create(self, **kw):
        conn = sqlite3.connect("newDB.db")
        cursor = conn.cursor()
        command = f'INSERT INTO {self.model_cls._table_name}('
        for k, v in self.model_cls._fields.items():
            if isinstance(v, Field):
                command += k + ', '

        command = command[:-2] + ') VALUES ('

        for k, v in self.model_cls._fields.items():
            if isinstance(v, Field):
                command += '?, '
        command = command[:-2] + ')'
        cursor.execute(command, [kw[k] for k, v in self.model_cls._fields.items() if isinstance(v, Field)])

        conn.commit()

    def all(self):
        conn = sqlite3.connect("newDB.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        command = f'select * from  {self.model_cls._table_name}'
        res = cursor.execute(command)
        return [self.model_cls(**item) for item in res]

    def filter(self, **kwargs):
        return QuerySet(self.model_cls, **kwargs)


class Model(metaclass=ModelMeta):
    _fields = {}
    _table_name = ''

    class Meta:
        table_name = ''

    objects = Manage()

    # todo DoesNotExist
    # DoesNotExist = DoesNotExistDescrt('1')

    def __init__(self, *_, **kwargs):
        for field_name, field in self._fields.items():
            value = field.validate(kwargs.get(field_name))
            setattr(self, field_name, value)
        if 'raw_id' in kwargs.keys():
            self.raw_id = kwargs['raw_id']
        else:
            self.raw_id = None

    def save(self):
        conn = sqlite3.connect("newDB.db")
        cursor = conn.cursor()
        if self.raw_id is None:

            command = f'INSERT INTO {self._table_name}('
            for k, v in self._fields.items():
                if isinstance(v, Field):
                    command += k + ', '

            command = command[:-2] + ') VALUES ('

            for k, v in self._fields.items():
                if isinstance(v, Field):
                    command += '\'' + str(getattr(self, k)) + '\', '
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
            conn = sqlite3.connect("newDB.db")
            cursor = conn.cursor()
            command = f"DELETE FROM {self._table_name} WHERE raw_id = {self.raw_id}"
            cursor.execute(command)
            conn.commit()
