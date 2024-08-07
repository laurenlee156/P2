import keyword
from collections import defaultdict

# compute a large string that describes the class, and return the class object it represents
def mynamedtuple(type_name, field_names, mutable = False, defaults = {}):
    # checks if the first character of type_name is a letter
    if not(type_name.split()[0].isalpha()):
        raise SyntaxError('type_name must begin with a letter.')
    # checks if any part of type_name is a Python keyword
    elif any(name in type_name for name in keyword.kwlist):
        raise SyntaxError('type_name cannot contain a Python keyword.')

    # checks if field_names is a list or string
    elif type(field_names) is not str and type(field_names) is not list:
        raise SyntaxError('field_names must be of type string or list.')

    # filters out duplicate names by converting field_names into a set
    field_names = {i for i in field_names}

    # checks the keys in default dictionary with field_names
    # if field_names not in defaults.keys():
    #     raise SyntaxError('Key in defaults does not match field_names.')

    # init method


class coordinate:
    _fields = ['x', 'y']
    _mutable = False

    def __init__(self, x, y):
        self.x = x
        self.y = y



# def __repr__(self):
#     return f"coordinate('x={self.x}, y={self.y}')"




print(mynamedtuple("hi", 'y,x', mutable = False))

