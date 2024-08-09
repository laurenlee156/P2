import keyword

# compute a large string that describes the class, and return the class object it represents
def mynamedtuple(type_name, field_names, mutable = False, defaults = {}):
    # checks if any part of type_name is a Python keyword
    if type_name in keyword.kwlist:
        raise SyntaxError('type_name cannot be a Python keyword.')
    # checks if the first character of type_name is a letter
    elif not (type_name[0].isalpha()):
        raise SyntaxError('type_name must begin with a letter.')

    field_names_lst = []
    if type(field_names) is list:
        for field in field_names:
            if field in keyword.kwlist or not field[0].isalpha():
                raise SyntaxError('field_name is invalid.')
            elif field not in field_names_lst:
                field_names_lst.append(field)

    elif type(field_names) is str:
        if len(field_names) > 1:
            if ',' in field_names:
                field_names = field_names.split(', ')
                for field in field_names:
                    if field in keyword.kwlist or not field[0].isalpha():
                        raise SyntaxError('field_name is invalid.')
                    elif field not in field_names_lst:
                        field_names_lst.append(field)
            else:
                field_names = field_names.split(' ')
                for field in field_names:
                    if field in keyword.kwlist or not field[0].isalpha():
                        raise SyntaxError('field_name is invalid.')
                    elif field not in field_names_lst:
                        field_names_lst.append(field)
        elif len(field_names) == 0:
            raise SyntaxError('field_names is empty.')
        else:
            if field_names in keyword.kwlist or not field_names[0].isalpha():
                raise SyntaxError('field_name is invalid.')
            elif field_names not in field_names_lst:
                field_names_lst.append(field_names)
    else:
        raise SyntaxError('field_names must be of type list or string.')

    # init method
    init_field_strings = ""
    for field in field_names_lst:
        init_field_strings += "self." + field + " = " + field + "\n" + "        "

    init_param_strings = ""
    for field in field_names_lst:
        if field in defaults:
            init_param_strings += field + " = " + str(defaults[field]) + ", "
        else:
            init_param_strings += field + ", "
    init_param_strings = init_param_strings[:-2]

    init_final_str = "class " + type_name + ":" + "\n"\
                     + "    " + "_fields = " + str(field_names) + "\n"\
                     + "    " + "_mutable = " + str(mutable) + "\n"\
                     + "    " + "def __init__(self, " + init_param_strings + "):" + "\n"\
                     + "        " + init_field_strings + "\n"

    # repr method
    repr_param_str = ""
    for param in field_names_lst:
        repr_param_str += f"{param} = self.{param}, "
    repr_param_str = repr_param_str[:-2]

    repr_final_str = ""
    repr_final_str += "    " + "def __repr__(self):\n"\
                      + "        " + "return " + "'" + type_name + "(" + repr_param_str + ")" + "'" + "\n"

    # query/accessor methods
    accessor_final_str = ""
    for field in field_names_lst:
        accessor_final_str += "    " + "def get_" + field + "(self):" + "\n"\
                              + "        " + "return self." + field + "\n"

    # indexing operator (unsure)
    indexing_final_str = ""
    indexing_final_str += "    " + "def __getitem__(self, index):" + "\n"\
                          + "        " + "if type(index) is int:" + "\n"\
                          + "            " + "return getattr(self, self._fields[index])" + "\n"\
                          + "        " + "else:" + "\n"\
                          + "            " + "raise TypeError" + "\n"

    # overload == operator
    eq_final_str = ""
    eq_final_str += "    " + "def __eq__(self, other):" + "\n"\
                    + "        " + ("if type(self) == type(other) " 
                                    "and self.__dict__ == other.__dict__:") + "\n"\
                    + "            " + "return True" + "\n"\
                    + "        " + "else:" + "\n"\
                    + "            " + "return False" + "\n"

    # _asdict method
    as_dict_final_str = ""
    as_dict_final_str += "    " + "def _asdict(self):" + "\n"\
                         + "        " + "return self.__dict__" + "\n"

    make_method_str = ""
    make_method_str += "    " + "def _make(iterable):" + "\n"\
                       + "        " + "if len(iterable) != len(self._fields):" + "\n"\
                       + "          " + "raise ValueError('iterable length does not match _fields length')" + "\n"\
                       + "        " + "else:" + "\n"\
                       + "          " + "return self.__class__(*iterable)" + "\n"

    # _replace method
    replace_method_str = ""
    replace_method_str += "    " + "def _replace(self, **kargs):" + "\n"\
                          + "        " + "if self._mutable:" + "\n"\
                          + "          " + "for key in kargs:" + "\n"\
                          + "              " + "if key in self.__dict__:" + "\n"\
                          + "                  " + "self.__dict__[key] = kargs[key]" + "\n"\
                          + "          " + "return None" + "\n"\
                          + "        " + "else:" + "\n"\
                          + "          " + "return type(self)(**kargs)"

    # __setattr__ method
    # first check if other methods are right

    final_str = init_final_str + repr_final_str + accessor_final_str + indexing_final_str + eq_final_str + as_dict_final_str + make_method_str + replace_method_str
    #print(final_str)
    exec(final_str, locals())
    return locals().get(type_name)

#
# coordinate = mynamedtuple('coordinate', 'x y')
# p = coordinate(0, 0)
# print(p)
# print(repr(p))
# print(p._asdict())

class DictTuple:
    def __init__(self, *args):
        if len(args) == 0:
            raise AssertionError("DictTuple.__init__: There must be at least one dictionary.")
        for arg in args:
            if type(arg) is not dict:
                raise AssertionError("DictTuple.__init__: Each argument must be a dictionary.")
            if len(arg) == 0:
                raise AssertionError("DictTuple.__init__: Dictionary cannot be empty")
        self.dt = list(args)
        print(self.dt)
    # count number of distinct keys
    def __len__(self):
        distinct_key_lst = []
        for dictionary in self.dt:
            print(dictionary)
            for key in dictionary:
                print(key)
                if key not in distinct_key_lst:
                    distinct_key_lst.append(key)
        return len(distinct_key_lst)

    def __bool__(self):
        if len(self.dt) > 1:
            return True
        else:
            return False

    def __repr__(self):
        repr_str = ""
        for dictionary in self.dt:
            repr_str += str(dictionary) + ", "
        repr_str = repr_str[:-2]
        return f"DictTuple({repr_str})"

    def __contains__(self, item):
        for dictionary in self.dt:
            if item in dictionary:
                return True
            else:
                return False

    #def __getitem__(self, index):

# o = DictTuple({'c1': 2}, {'c1': 3})
# print(o.__bool__())
# print(o.__repr__())
# print(o.__contains__('c2'))