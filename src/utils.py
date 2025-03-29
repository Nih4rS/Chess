# Helper functions to handle repeated tasks
import os

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
