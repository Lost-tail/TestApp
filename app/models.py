from datetime import date
from email.generator import Generator
from services import Converter
import fields


class BaseModel:

    def __init__(self, *args, **kwargs) -> None:
        i = 0
        if args:
            for name, field in self.__class__.__dict__.items():
                if isinstance(field, fields.Field):
                    setattr(self, name, args[i])
                    i = i + 1 
                    if i >= len(args): break
                    
        for key, value in kwargs.items():
            setattr(self, key, value)
        if hasattr(self, '__post_init__'):
            self.__post_init__()


    @classmethod
    def sql_description(cls) -> str:
        items = []
        for key, field in cls.__dict__.items():
            if isinstance(field, fields.Field):
                items.append(field.sql_description())
        return ', '.join(items + [f"PRIMARY KEY ({cls.pk_field})"])

    @classmethod
    def columns(cls):
        return [key for key, field in cls.__dict__.items() if isinstance(field, fields.Field)]

    def __repr__(self):
        return str(tuple([v for k, v in self.__dict__.items()]))

    def get_data(self) -> Generator:
        return (v for k, v in self.__dict__.items())


class Order(BaseModel):

    order_id = fields.IntField()
    order_number = fields.IntField()
    price_usd = fields.FloatField()
    delivery_time = fields.DateField()
    price_rub = fields.FloatField(default=0)
    pk_field = 'order_id'

    def __post_init__(self) -> None:
        self.price_rub = Converter.usd_to_rub(self.price_usd)

