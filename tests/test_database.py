import sqller

import sqller as utils
import pytest


class TestDatabaseUtils:
    def test_model_creation_convetion_violation_fields(self):
        with pytest.raises(utils.ConventionViolationError):
            class Chat(metaclass=utils.ModelMeta):
                NAME = 'chats'

    def test_model_creation_convetion_violation_name(self):
        with pytest.raises(utils.ConventionViolationError):
            class Chat(metaclass=utils.ModelMeta):
                FIELDS = [
                    utils.Field(name="id", dtype="integer",
                                postfix="PRIMARY KEY"),
                    utils.Field(name="type", dtype="text"),
                    utils.Field(name="last_name", dtype="text"),
                    utils.Field(name="first_name", dtype="text"),
                    utils.Field(name="username", dtype="text")
                ]

    def test_model_creation_all_class_attributes(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        assert hasattr(Chat, 'sql_create_table_if_not_exists')

    def test_model_creation_all_object_attributes(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]
        obj = Chat(
            id=0,
            type='usual',
            last_name='Vouk',
            first_name='Ilya',
            username='voilalex'
        )

        assert hasattr(obj, 'id') and obj.id == 0
        assert hasattr(obj, 'type') and obj.type == 'usual'
        assert hasattr(obj, 'last_name') and obj.last_name == 'Vouk'
        assert hasattr(obj, 'first_name') and obj.first_name == 'Ilya'
        assert hasattr(obj, 'username') and obj.username == 'voilalex'

    def test_model_reference_violation(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]
        with pytest.raises(Exception):
            Chat.reference('not_existing_field')

    def test_model_reference(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]
        assert Chat.reference('id') == 'chats(id)'

    def test_dao_creation(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        class ChatDAO(metaclass=utils.DAOMeta):
            MODEL = Chat

    def test_dao_sql_get_one(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        class ChatDAO(metaclass=utils.DAOMeta):
            MODEL = Chat

        assert ChatDAO.sql_get_one(
            0) == 'SELECT * FROM chats\nWHERE id = 0\nLIMIT 1;'

    def test_dao_sql_find_all(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        class ChatDAO(metaclass=utils.DAOMeta):
            MODEL = Chat

        assert ChatDAO.sql_find_all() == 'SELECT * FROM chats;'

    def test_dao_sql_save(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        class ChatDAO(metaclass=utils.DAOMeta):
            MODEL = Chat

        obj = Chat(
            type='usual',
            last_name='Vouk',
            first_name='Ilya',
            username='voilalex'
        )

        assert ChatDAO.sql_save(
            obj) == "INSERT INTO chats(type,last_name,first_name,username)\nVALUES ('usual','Vouk','Ilya','voilalex')"

    def test_dao_sql_exists(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        class ChatDAO(metaclass=utils.DAOMeta):
            MODEL = Chat

        obj = Chat(
            type='usual',
            last_name='Vouk',
            first_name='Ilya',
            username='voilalex'
        )

        assert ChatDAO.sql_exists(
            obj) == "SELECT count(*) FROM chats WHERE type = 'usual' AND last_name = 'Vouk' AND first_name = 'Ilya' AND username = 'voilalex';"

    def test_dao_sql_custom_query_anonymous_1(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        class ChatDAO(metaclass=utils.DAOMeta):
            MODEL = Chat
            sql_find_all_by_type = utils.CustomQuery()

        assert ChatDAO.sql_find_all_by_type(
            type='usual') == "SELECT * FROM chats WHERE type = 'usual'"

    def test_dao_sql_custom_query_anonymous_2(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        class ChatDAO(metaclass=utils.DAOMeta):
            MODEL = Chat
            sql_delete_all_by_type = utils.CustomQuery()

        assert ChatDAO.sql_delete_all_by_type(
            type='usual') == "DELETE FROM chats WHERE type = 'usual'"

    def test_dao_sql_custom_query_anonymous_3(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        class ChatDAO(metaclass=utils.DAOMeta):
            MODEL = Chat
            sql_delete_by_type = utils.CustomQuery()

        assert ChatDAO.sql_delete_by_type(
            type='usual') == "DELETE FROM chats WHERE type = 'usual'"

    def test_dao_sql_custom_query_anonymous_4(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        with pytest.raises(sqller.exceptions.CustomSQLBuildError):
            class ChatDAO(metaclass=utils.DAOMeta):
                MODEL = Chat
                sql_delete_by_type_name = utils.CustomQuery()

    def test_dao_sql_custom_query_anonymous_5(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        class ChatDAO(metaclass=utils.DAOMeta):
            MODEL = Chat
            sql_delete_by_type = utils.CustomQuery()
            sql_find_all_by_last_name_and_first_name = utils.CustomQuery()

        assert ChatDAO.sql_delete_by_type(type='type') == "DELETE FROM chats WHERE type = 'type'"
        assert ChatDAO.sql_find_all_by_last_name_and_first_name(
            first_name='Ilya',
            last_name='Vouk'
        ) == "SELECT * FROM chats WHERE last_name = 'Vouk' AND first_name = 'Ilya'"


    def test_dao_sql_custom_query_user_provided_1(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        class ChatDAO(metaclass=utils.DAOMeta):
            MODEL = Chat
            custom_find = utils.CustomQuery(
                "SELECT * FROM chats WHERE last_name = Vouk")

        assert ChatDAO.custom_find() == "SELECT * FROM chats WHERE last_name = Vouk"

    def test_dao_sql_update(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        class ChatDAO(metaclass=utils.DAOMeta):
            MODEL = Chat

        obj = Chat(
            id=0,
            type='usual',
            last_name='Vouk',
            first_name='Ilya',
            username='voilalex'
        )

        assert ChatDAO.sql_update(
            obj) == "UPDATE chats SET type='usual', last_name='Vouk', first_name='Ilya', username='voilalex'\nWHERE id=0"

    def test_dao_sql_delete_by_id(self):
        class Chat(metaclass=utils.ModelMeta):
            NAME = 'chats'
            FIELDS = [
                utils.Field(name="id", dtype="integer",
                            postfix="PRIMARY KEY"),
                utils.Field(name="type", dtype="text"),
                utils.Field(name="last_name", dtype="text"),
                utils.Field(name="first_name", dtype="text"),
                utils.Field(name="username", dtype="text")
            ]

        class ChatDAO(metaclass=utils.DAOMeta):
            MODEL = Chat

        assert ChatDAO.sql_delete_by_id(1) == 'DELETE FROM chats\nWHERE id=1'
