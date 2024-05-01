# utils.py
import random
import string

def generate_customer_id(prefix="CO", length=8):
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix} {random_chars}"
