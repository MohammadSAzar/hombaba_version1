import re


def name_checker(name):
    pattern = r'^[آ-ی\s]+$'
    return re.match(pattern, name) is not None


