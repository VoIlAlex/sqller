# Sqller

ORM library to build SQLite based application in format model/dao/service.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Installing

To install the package type the following in your terminal:

```bash
sudo pip install sqller
```

## Usage

### Model definition

Example of model definition.

```python
class Chat(metaclass=ModelMeta):
    NAME = 'chats'
    FIELDS = [
        Field(name="id", dtype="integer", postfix="PRIMARY KEY"),
        Field(name="type", dtype="text"),
        Field(name="last_name", dtype="text"),
        Field(name="first_name", dtype="text"),
        Field(name="username", dtype="text")
    ]
```

It will generate constructor and sql returning methods.

### Data Access Object (DAO) definition

Example of DAO definition.

```python
class ChatDAO(metaclass=DAOMeta):
    MODEL = Chat

```

It will generate static methods to generate sql text for accessing fields in `Chat` table.

### Service definition

Example of Service definition.

```python
class TelegramService(metaclass=ServiceMeta):
    DB_PATH = 'telegram.db'
    MODELS = [
        models.Chat,
        models.SelectedCriterion
    ]

    @staticmethod
    def connect() -> sqlite3.Connection: ...

    @staticmethod
    def save_predefined_chat():
        connection = TelegramService.connect()
        obj = Chat(
            id=0,
            type='usual',
            last_name='Vouk',
            first_name='Ilya',
            username='voilalex'
        )
        sql_save = ChatDAO.sql_save(obj)
        cursor = connection.cursor()
        cursor.execute(sql_save)
        result = cursor.fetchall()
        print(result)
        connection.commit()
```

It will automatically generate database with the name defined in `DB_PATH` constant with all the required tables and create connect function to connect to that database.

## Running the tests

To run tests type the following in your terminal:

```bash
python3 -m pytest
```

or

```bash
python -m pytest
```

if the previous command doesn't work.

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

- **Ilya Vouk** - _Initial work_ - [VoIlAlex](https://github.com/VoIlAlex)

See also the list of [contributors](https://github.com/VoIlAlex/sqller/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
