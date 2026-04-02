import os
import sys

def get_resource_path(relative_path):
    """ Get the absolute path to the resource, works for development and for PyInstaller """
    try:
        # PyInstaller creates a `_MEIPASS` folder in the temporary directory
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# The rest of the LTF Editor GUI code goes here...
