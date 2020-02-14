from enum import Enum


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

    @classmethod
    def folders_list(cls):
        return [p.folder_name for p in cls]