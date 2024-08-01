import sys
import os 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.login import login_to_youtube

if __name__ == "__main__":
    login_to_youtube()
