import os
from get_data import baseCache

def clear_cache_files():
    dir = './'+baseCache
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

if __name__ == '__main__':
    clear_cache_files()