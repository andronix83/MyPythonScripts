import os
import shutil
import subprocess

from jetbrains.products import Product

USER_FOLDER = os.getenv("USERPROFILE")
assert USER_FOLDER is not None


def is_settings_folder(folder_name):
    return any([folder_name.startswith(f".{name}")
                for name in Product.folders_list()])


def remove_folder(folder_path):
    if os.path.isdir(folder_path):
        # this is necessary for removing non-empty folder
        # otherwise, use os.rmdir(path)
        # TODO: add exception handling
        shutil.rmtree(folder_path)
        print(f"Directory '{folder_path}' was removed!")
    else:
        print(f"Directory '{folder_path}' doesn't exist!")


def remove_string(src_file_path, search_string):
    tmp_file_path = src_file_path + ".tmp"

    with open(src_file_path, "r") as src_file:
        with open(tmp_file_path, "w") as tmp_file:
            for src_line in src_file:
                if search_string not in src_line:
                    tmp_file.write(src_line)

    os.remove(src_file_path)
    os.rename(tmp_file_path, src_file_path)


def remove_reg_key(reg_key_path):
    code = subprocess.call(f"reg delete \"{reg_key_path}\" /f")
    print(code)


if __name__ == '__main__':
    all_settings_folders = [f.path for f in os.scandir(USER_FOLDER)
                            if f.is_dir() and is_settings_folder(f.name)]

    all_installed_products = [Product.product_item(settings_path)
                              for settings_path in all_settings_folders]

    print("\nFound the following installed JetBrains products:")
    [print(f" - {product.product.folder_name} ({product.product.name})")
     for product in all_installed_products]

    product_codes_to_reset_str = input("\nEnter the product code(s) (separated by space) or ALL to reset trial: ")

    if product_codes_to_reset_str.strip().upper() == "ALL":
        products_to_reset = all_installed_products
    else:
        product_codes_to_reset = [code.upper() for code in product_codes_to_reset_str.split(sep=" ")]
        products_to_reset = [product for product in all_installed_products
                             if product.product.name in product_codes_to_reset]

    for product_item in products_to_reset:
        remove_folder(f"{product_item.settings_path}\\config\\eval")
        remove_string(f"{product_item.settings_path}\\config\\options\\other.xml", "evlsprt")
        remove_reg_key(f"HKEY_CURRENT_USER\\Software\\JavaSoft\\Prefs\\jetbrains\\{product_item.product.reg_key_name}")


# TODO Add logging to file (+ gitignore)
# TODO Add argparse (with all support)
# TODO Exception handling and more asserts
# TODO Correct comments in doc-style
# TODO move main code to class
# TODO use Popen and find the correct encoding
