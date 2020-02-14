from enum import Enum
from collections import namedtuple


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

    def __init__(self, folder_name, reg_key_name=None):
        self.folder_name = folder_name
        self.reg_key_name = reg_key_name if reg_key_name else folder_name.lower()

    def __str__(self):
        return f"Product.{self.name}(folder_name={self.folder_name}, reg_key_name={self.reg_key_name})"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def folders_list(cls):
        return [p.folder_name for p in cls]

    @classmethod
    def product_item(cls, settings_path):
        result_product = None
        # TODO: Think how to rewrite it in a more functional way
        for product in cls:
            if product.folder_name in settings_path:
                result_product = product
                break
        assert result_product is not None
        return ProductItem(result_product, settings_path)


ProductItem = namedtuple("ProductItem", ["product", "settings_path"])
