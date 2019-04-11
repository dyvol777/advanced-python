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
        comand = f"create table if not exists {meta.table_name}("
        for k, v in fields.items():
            if isinstance(v, StringField):
                comand += f'{k} text,'
            elif isinstance(v, IntField):
                comand += f'{k} integer,'
        comand += 'row_id integer PRIMARY KEY)'

        cursor.execute(comand.lower())

        return super().__new__(mcs, name, bases, namespace)


class QuerySet:
    def __init__(self, model_cls, conditions):
        self.model = model_cls
        self.conditions = conditions

    def get(self):
        q = f'select * from {self.model.table} where '

        res = conn.execute(q)
        return [self.model(**item) for item in res]

    def filter(self):
        #modify cond
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
                command += '\'' + str(kw[k]) + '\', '
        command = command[:-2]
        command += ')'
        cursor.execute(command)
        conn.commit()

    def all(self):
        conn = sqlite3.connect("newDB.db")
        cursor = conn.cursor()
        command = f'INSERT INTO {self.model_cls._table_name}('
        for k, v in self.model_cls._fields.items():
            if isinstance(v, Field):
                command += k + ', '

        command = command[:-2] + ') VALUES ('

        for k, v in self.model_cls._fields.items():
            if isinstance(v, Field):
                command += '\'' + str(kw[k]) + '\', '
        command = command[:-2]
        command += ')'
        cursor.execute(command)

    def get(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass 

    def filter(self, **q):
        return QuerySet(self.model_cls, **q)


class DoesNotExistDescrt:
    exceptions = {}

    def __init__(self, text):
        self.txt = text

    def __get__(self, instance, mdl_cls):
        if mdl_cls in exceptions:
            return exceptions[mdl_cls]
        else:
            cls = type('DoesNotExist', Exception, {'model': mdl_cls})
            exceptions[mdl_cls] = cls
            return cls


class Model(metaclass=ModelMeta):
    _fields = {}

    class Meta:
        table_name = ''

    objects = Manage()

    # todo DoesNotExist
    DoesNotExist = DoesNotExistDescrt('1')

    def __init__(self, *_, **kwargs):
        for field_name, field in self._fields.items():
            value = field.validate(kwargs.get(field_name))
            setattr(self, field_name, value)
        self._fields['primary_key'] = None

    def save(self):
        if self._fields['primary_key'] is None:
            pass
        else:
            pass

    def delete(self):
        if self._fields['primary_key'] is None:
            del self
        else:
            pass
