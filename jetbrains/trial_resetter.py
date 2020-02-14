import os
import shutil
import subprocess

SUPPORTED_PRODUCTS = [
    "IntelliJIdea",
    "PyCharm",
    "WebStorm",
    "DataGrip",
    "RubyMine"]

USER_FOLDER = os.getenv("USERPROFILE")
assert USER_FOLDER is not None


def is_settings_folder(folder_name):
    return any([folder_name.startswith(f".{name}")
                for name in SUPPORTED_PRODUCTS])


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
    test_product = "DataGrip"

    all_settings_folders = [f.path for f in os.scandir(USER_FOLDER)
                            if f.is_dir() and is_settings_folder(f.name)]
    test_product_settings_folders = [f.path for f in os.scandir(USER_FOLDER)
                                     if f.is_dir() and f.name.startswith(f".{test_product}")]

    for settings_folder in test_product_settings_folders:
        remove_folder(f"{settings_folder}\\config\\eval")
        remove_string(f"{settings_folder}\\config\\options\\other.xml", "evlsprt")
        remove_reg_key(f"HKEY_CURRENT_USER\\Software\\JavaSoft\\Prefs\\jetbrains\\{test_product.lower()}")

# TODO Add Enum with exclusion for "idea"
# TODO Add logging to file (+ gitignore)
# TODO Add argparse (with all support)
# TODO Show detected products (by settings folder)
# TODO Add interactive mode if no args provided
# TODO Exception handling and more asserts
# TODO Correct comments in doc-style
