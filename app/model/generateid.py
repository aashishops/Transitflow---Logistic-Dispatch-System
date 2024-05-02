import random
import string

def generate_id(prefix, length):
    random_digits = ''.join(random.choices(string.digits, k=length))
    return f"{prefix+random_digits}"