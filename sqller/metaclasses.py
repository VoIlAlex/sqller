import sqlite3
from .exceptions import ConventionViolationError
from .utils import CustomQuery, Field, is_empty_function


class ModelMeta(type):
    """Metaclass for all the datamodels.
    Generates default __init__ with all the arguments.
    Generates queries for the model. And generates few more
    utilities to use in workflow of database table.

    Requires class of the metaclass to have defined:
        - `NAME` - name of the database table.
        - `FIELDS` - list of fields in the table.
    """
    def __new__(cls, name, bases, dct):
        c = type.__new__(cls, name, bases, dct)

        generators = ModelMeta.__get_all_generators()
        for g in generators:
            g(c, name, bases, dct)
        return c

    @staticmethod
    def __get_all_generators():
        generators = []
        for attr_name in ModelMeta.__dict__:
            attr = ModelMeta.__dict__[attr_name]
            if isinstance(attr, staticmethod):
                if '__generate' in attr.__func__.__name__ and attr.__func__.__code__.co_argcount == 4:
                    generators.append(attr.__func__)
        return generators

    @staticmethod
    def __generate_create_table_if_not_exists(cls, name, bases, dct):
        if not 'FIELDS' in dct or not 'NAME' in dct:
            raise ConventionViolationError

        @staticmethod
        def sql_create_table_if_not_exists():
            sql_query = f"CREATE TABLE IF NOT EXISTS {dct['NAME']}("
            for field in dct['FIELDS']:
                sql_query += field.sql_description() + ",\n"
            sql_query = sql_query[:-2]
            sql_query += ")"
            return sql_query
        setattr(cls, 'sql_create_table_if_not_exists',
                sql_create_table_if_not_exists)

    @staticmethod
    def __generate_all_arguments_constructor(cls, name, bases, dct):
        if not 'FIELDS' in dct:
            raise ConventionViolationError

        def init(self, *args, **kwargs):
            for field in dct['FIELDS']:
                value = kwargs.get(field.name, None)
                setattr(self, field.name, value)
        cls.__init__ = init

    @staticmethod
    def __generate_reference(cls, name, bases, dct):
        if not 'FIELDS' in dct or not 'NAME' in dct:
            raise ConventionViolationError

        @staticmethod
        def reference(name: str):
            field = [f for f in dct['FIELDS'] if f.name == name][0]
            return f"{dct['NAME']}({field.name})"
        cls.reference = reference


class DAOMeta(type):
    def __new__(cls, name, bases, dct):
        c = type.__new__(cls, name, bases, dct)
        generators = DAOMeta.__get_all_generators()
        for g in generators:
            g(c, name, bases, dct)
        return c

    @staticmethod
    def __get_all_generators():
        generators = []
        for attr_name in DAOMeta.__dict__:
            attr = DAOMeta.__dict__[attr_name]
            if isinstance(attr, staticmethod):
                if '__generate' in attr.__func__.__name__ and attr.__func__.__code__.co_argcount == 4:
                    generators.append(attr.__func__)
        return generators

    @staticmethod
    def __generate_get_one(cls, name, bases, dct):
        for field in dct['MODEL'].FIELDS:
            if field.name == 'id':
                break
        else:
            raise RuntimeError(
                "Model should have `id` field for DAOMeta generation.")

        @staticmethod
        def sql_get_one(id: int) -> str:
            sql_query = f"SELECT * FROM {dct['MODEL'].NAME}\nWHERE id = {id}\nLIMIT 1;"
            return sql_query
        cls.sql_get_one = sql_get_one

    @staticmethod
    def __generate_find_all(cls, name, bases, dct):
        @staticmethod
        def sql_find_all() -> str:
            sql_query = f"SELECT * FROM {dct['MODEL'].NAME};"
            return sql_query
        cls.sql_find_all = sql_find_all

    @staticmethod
    def __generate_save(cls, name, bases, dct):
        @staticmethod
        def sql_save(obj: dct['MODEL']) -> str:
            sql_query_start = f"INSERT INTO {dct['MODEL'].NAME}("
            sql_query_end = 'VALUES ('
            for field in dct['MODEL'].FIELDS:
                if getattr(obj, field.name) != None and field.name != 'id':
                    sql_query_start += f'{field.name},'
                    sql_query_end += f'{getattr(obj, field.name)},' if field.dtype != 'text' else f"'{getattr(obj, field.name)}',"
            sql_query = sql_query_start[:-1] + \
                ')' + '\n' + sql_query_end[:-1] + ')'
            return sql_query
        cls.sql_save = sql_save

    @staticmethod
    def __generate_exists(cls, name, bases, dct):
        @staticmethod
        def sql_exists(obj: dct['MODEL']) -> str:
            sql_query = f"SELECT count(*) FROM {dct['MODEL'].NAME} WHERE "
            i = 0
            for field in dct['MODEL'].FIELDS:
                if getattr(obj, field.name) is not None and field.name != 'id':
                    if i != 0:
                        sql_query += " AND "
                    sql_value = f"{getattr(obj, field.name)}" if field.dtype != 'text' else f"'{getattr(obj, field.name)}'"
                    sql_query += f"{field.name} = {sql_value}"
                    i += 1
            sql_query += ";"
            return sql_query
        cls.sql_exists = sql_exists

    @staticmethod
    def __generate_custom_queries(cls, name, bases, dct):
        for attr_name in dct:
            if isinstance(dct[attr_name], CustomQuery):
                if dct[attr_name].query is None and attr_name.startswith('sql_'):
                    keys = []
                    sql_query_template = ''
                    lexems = attr_name[4:].split('_')
                    sep = ' '
                    for lex in lexems:
                        if lex == 'select' or lex == 'find':
                            sep = ','
                            sql_query_template += 'SELECT '
                        elif lex == 'all':
                            sep = ' '
                            sql_query_template += '*' + sep
                            sql_query_template += f"FROM {dct['MODEL'].NAME}" + sep
                        elif lex == 'by':
                            sep = ' '
                            sql_query_template += 'WHERE' + sep
                        elif lex == 'and':
                            sep = ' '
                            sql_query_template += 'AND' + sep
                        else:
                            if sql_query_template[-1] != sep:
                                sql_query_template += sep
                            sql_query_template += lex + ' = {}'
                            keys.append(lex)

                    @staticmethod
                    def sql_custom_query(*args, **kwargs):
                        sql_query = sql_query_template
                        for key in keys:
                            sql_query = sql_query.format(kwargs[key])
                        return sql_query
                    setattr(cls, attr_name, sql_custom_query)
                elif dct[attr_name].query is not None:
                    @staticmethod
                    def sql_custom_query(*args):
                        sql_query = dct[attr_name].query
                        for arg in args:
                            sql_query = sql_query.format(arg)
                        return sql_query
                    setattr(cls, attr_name, sql_custom_query)
                else:
                    raise ConventionViolationError


class ServiceMeta(type):
    def __new__(cls, name, bases, dct):
        c = type.__new__(cls, name, bases, dct)

        generators = ServiceMeta.__get_all_generators()
        for g in generators:
            g(c, name, bases, dct)
        return c

    @staticmethod
    def __get_all_generators():
        generators = []
        for attr_name in ServiceMeta.__dict__:
            attr = ServiceMeta.__dict__[attr_name]
            if isinstance(attr, staticmethod):
                if '__generate' in attr.__func__.__name__ and attr.__func__.__code__.co_argcount == 4:
                    generators.append(attr.__func__)
        return generators

    @staticmethod
    def __generate_connect(cls, name, bases, dct):
        @staticmethod
        def connect():
            connection = None
            try:
                connection = sqlite3.connect(dct['DB_PATH'])
            except sqlite3.Error as e:
                print(e)
            if connection is not None:
                try:
                    cursor = connection.cursor()
                    for table in dct['MODELS']:
                        cursor.execute(
                            table.sql_create_table_if_not_exists())
                except sqlite3.Error as e:
                    print(e)
            return connection
        cls.connect = connect
