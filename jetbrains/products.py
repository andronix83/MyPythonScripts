from collections import namedtuple
from enum import Enum
from typing import List

ProductItem = namedtuple("ProductItem", ["product", "settings_path"])


class Product(Enum):

    CL = ("CLion",)
    DG = ("DataGrip",)
    GO = ("GoLand",)
    IJ = ("IntelliJIdea", "idea")
    PS = ("PhpStorm",)
    PC = ("PyCharm",)
    RD = ("Rider",)
    RM = ("RubyMine",)
    WS = ("WebStorm",)

    def __init__(self, folder_name: str, reg_key_name: str = None):
        self.folder_name = folder_name
        self.reg_key_name = reg_key_name if reg_key_name else folder_name.lower()

    def __str__(self):
        return f"Product.{self.name}({self.folder_name=}, {self.reg_key_name=})"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def folders_list(cls) -> List[str]:
        if not hasattr(cls, "_folders_list"):
            cls._folders_list = [p.folder_name for p in cls]
        return cls._folders_list

    @classmethod
    def product_item(cls, settings_path: str) -> ProductItem:
        found_product = next(p for p in cls if p.folder_name in settings_path)
        return ProductItem(found_product, settings_path)



