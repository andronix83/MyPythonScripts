import os
import shutil

from jetbrains.products import Product, ProductItem

# this script is intended for v. 2020.1 or newer
class TrialResetter:

    USER_FOLDER = os.getenv("USERPROFILE")
    assert USER_FOLDER is not None

    @classmethod
    def start(cls):
        settings_dir = os.path.join(cls.USER_FOLDER, "AppData", "Roaming", "JetBrains")

        all_settings_folders = None
        if os.path.exists(settings_dir):
            all_settings_folders = [f.path for f in os.scandir(settings_dir)
                                    if f.is_dir() and cls.__is_settings_folder(f.name)]

        if not all_settings_folders:
            print("No JetBrains products were found on this computer!")
            exit(0)

        all_installed_products = [Product.product_item(settings_path)
                                  for settings_path in all_settings_folders]

        print("\nFound the following installed JetBrains products (v.2020.1 or newer):")
        for product in all_installed_products:
            print(f" - {product.product.folder_name} ({product.product.name})")

        product_codes_to_reset_str = input("\nEnter the product code(s) (separated by space) or ALL to reset trial: ")

        if product_codes_to_reset_str.strip().upper() == "ALL":
            products_to_reset = all_installed_products
        else:
            product_codes_to_reset = [code.strip().upper() for code in product_codes_to_reset_str.split(sep=" ")]
            products_to_reset = [product for product in all_installed_products
                                 if product.product.name in product_codes_to_reset]

        if not products_to_reset:
            print("No installed products selected for trial reset!")
            exit(0)

        for product_item in products_to_reset:
            cls.__reset_product(product_item)

    @classmethod
    def __reset_product(cls, product_item: ProductItem) -> None:
        print(f"##### Resetting {product_item.product.folder_name} #####")
        cls.__remove_folder(os.path.join(product_item.settings_path, "eval"))
        cls.__remove_string(os.path.join(product_item.settings_path, "options", "other.xml"), "evlsprt")

    @classmethod
    def __is_settings_folder(cls, folder_name: str) -> bool:
        return next((True for name in Product.folders_list()
                     if folder_name.startswith(name)), False)

    @classmethod
    def __remove_folder(cls, folder_path: str) -> None:
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)  # for removing non-empty folder
            print(f"- Directory '{folder_path}' was removed!")

    @classmethod
    def __remove_string(cls, src_file_path: str, search_string: str) -> None:
        tmp_file_path = src_file_path + ".tmp"

        with open(src_file_path, "r") as src_file, open(tmp_file_path, "w") as tmp_file:
            for src_line in src_file:
                if search_string not in src_line:
                    tmp_file.write(src_line)

        os.remove(src_file_path)
        os.rename(tmp_file_path, src_file_path)
        print(f"- Evaluation key was removed from '{src_file_path}'")


if __name__ == '__main__':
    TrialResetter().start()


# TODO Add argparse (with all support)
# TODO Exception handling and more asserts
# TODO Correct comments in doc-style
