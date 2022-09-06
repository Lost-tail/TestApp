from datetime import date
from typing import Union, Callable



class Validation:

    def __init__(self, validation_function, convert_function, error_msg: str):
        self.validation_function = validation_function
        self.convert_function = convert_function
        self.error_msg = error_msg

    def __call__(self, value):
        if not self.validation_function(value):
            try:
                return self.convert_function(value)
            except:
                raise ValueError(f"{value!r} {self.error_msg}")
        return value


class Field():

    def __init__(self, default: Union[Callable, int, str]=None, is_null=False) -> None:
        self._name = None
        self._default = default
        self.is_null = is_null

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not instance.__dict__.get(self._name, None):
            setattr(instance, self._name, self._default() if callable(self._default) else self._default)
        return  instance.__dict__[self._name]

    def validate(self, value):
        return self.validation(value)

    def __set__(self, instance, value):
        value = self.validate(value)
        instance.__dict__[self._name] = value

    def sql_description(self) -> bytes:
        return f"{self._name} {self.sql_type} {'NOT NULL' if not self.is_null else ''}"

    def deserialize(self, obj):
        return self.deserialize_func(obj)


class StringField(Field):

    validation = Validation(lambda x: isinstance(x, str), lambda x: str(x), "is not a string")

    def __init__(self, length: int, *args, **kwargs):
        self.sql_type = f"VARCHAR({length})"
        super().__init__(*args, **kwargs)



class IntField(Field):
    
    sql_type = "INTEGER"
    validation = Validation(lambda x: isinstance(x, int), lambda x: int(x), "is not an int number")


class FloatField(Field):
    
    sql_type = "REAL"
    validation = Validation(lambda x: isinstance(x, (float, int)), lambda x: float(x), "is not a number")



class DateField(Field):
    
    sql_type = "DATE"
    validation = Validation(lambda x: isinstance(x, date), lambda x: date(*[int(y) for y in x.split('.')[::-1]]), "is not an int number")