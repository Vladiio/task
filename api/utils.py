import random
import string


def gen_random_string(max_length=20,
                      chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(max_length))


def get_token(response):
    return 'Token ' + response.data.get('token')
