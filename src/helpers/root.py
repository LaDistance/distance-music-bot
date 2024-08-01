import os
import inspect

def get_project_root() -> str:
    current_file = inspect.getfile(inspect.currentframe())
    current_dir = os.path.dirname(os.path.abspath(current_file))
    return os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))