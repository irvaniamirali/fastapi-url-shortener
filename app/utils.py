import random
import string

def generate_random_string(length=6):
    letters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string
