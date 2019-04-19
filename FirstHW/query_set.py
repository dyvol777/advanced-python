class QuerySet:
    def __init__(self, model_cls, **conditions):
        self.model = model_cls
        self.conditions = conditions

    def __iter__(self):
        pass

    def get(self):
        conn = self.model._conn

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
        conn = self.model._conn
        cursor = conn.cursor()
        command = f'delete from {self.model._table_name} where '
        for k, v in self.conditions.items():
            command += k + ' = \'' + str(v) + '\' and '
        command = command[:-5]
        cursor.execute(command)
        conn.commit()
