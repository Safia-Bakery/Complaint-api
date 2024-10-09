import random
import string

def file_name_generator(length=20):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
