
class CustomQuery:
    def __init__(self, query: str = None):
        self.query = query


class Field:
    def __init__(self, name: str, dtype: str, postfix: str = None, prefix: str = None, reference: str = None):
        self.name = name
        self.dtype = dtype
        self.postfix = postfix
        self.prefix = prefix
        self.reference = reference

    def sql_description(self) -> str:
        """Field description used in creation script

        Returns:
            str -- description used in creation script.
        """
        sql_field = self.prefix if self.prefix is not None else ''
        sql_field += f"{self.name} {self.dtype}"
        if self.postfix is not None:
            sql_field += f" {self.postfix}"
        if self.reference is not None:
            sql_field += f",\nFOREIGN KEY ({self.name}) REFERENCES {self.reference}"
        return sql_field


def is_empty_function(func):
    def empty_func():
        pass

    def empty_func_with_doc():
        """Empty function with docstring."""
        pass

    return func.__code__.co_code == empty_func.__code__.co_code or \
        func.__code__.co_code == empty_func_with_doc.__code__.co_code
