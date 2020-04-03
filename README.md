# Sqller

ORM library to build SQLite based application in format model/dao/service.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Installing

At first, you need SQLite3 to be installed. Type following in your terminal:

```bash
apt-get install libsqlite3-dev
```

To install the package type the following in your terminal:

```bash
sudo pip install sqller
```

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

## Usage

The usage of the library in real application consists of the following steps:

- Create a model
- Create a data access object (DAO)
- Create a service
- Use the service

The steps are described below.

### Create model

```python
class Chat(metaclass=sqller.ModelMeta):
    NAME = 'chats'
    FIELDS = [
        Field(name="id", dtype="integer", postfix="PRIMARY KEY"),
        Field(name="type", dtype="text"),
        Field(name="last_name", dtype="text"),
        Field(name="first_name", dtype="text"),
        Field(name="username", dtype="text"),
        Field(name="chat_id", dtype="integer")
    ]
```

### Create DAO

```python
class ChatDAO(metaclass=sqller.DAOMeta):
    MODEL = Chat
```

### Create service

```python
class TelegramService(metaclass=sqller.ServiceMeta):
    DB_PATH = config.DATABASE_PATH
    MODELS = [
        models.Chat,
        models.SelectedCriterion
    ]

    @staticmethod
    def save_chat_info(chat: telebot.types.Chat):
        obj_exist_checker = models.Chat(id=chat.id)
        obj = models.Chat(
            type = chat.type,
            last_name = chat.last_name,
            first_name = chat.first_name,
            username = chat.username,
            chat_id=chat.id
        )
        sql_exists = dao.ChatDAO.sql_exists(obj_exist_checker)
        sql_save = dao.ChatDAO.sql_save(obj)
        exists = TelegramService.execute(sql_exists)[0][0]
        if not exists:
            TelegramService.execute(sql_save)
```

### Use service

```python
TelegramService.save_chat_info(chat)
```

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

- **Ilya Vouk** - Initial work - [VoIlAlex](https://github.com/VoIlAlex)

See also the list of [contributors](https://github.com/VoIlAlex/sqller/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
