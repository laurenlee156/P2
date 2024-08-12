import keyword

def mynamedtuple(type_name, field_names, mutable = False, defaults = {}):
    # Checks if any part of type_name is a Python keyword.
    if type_name in keyword.kwlist:
        raise SyntaxError('type_name cannot be a Python keyword.')
    # Checks the type of type_name.
    elif type(type_name) is not str:
        raise SyntaxError('type_name must be a string.')
    # Checks if the first character of type_name is a letter.
    elif not type_name.strip() or not type_name.strip()[0].isalpha():
        raise SyntaxError('type_name must begin with a letter.')

    # Check exceptions for field_names.
    field_names_lst = []
    if type(field_names) is list:
        for field in field_names:
            # Checks if each field in field_names is a Python keyword, first character is not a letter,
            # or if it's not in field_names_lst.
            if field in keyword.kwlist or not field[0].isalpha() or field in field_names_lst:
                raise SyntaxError('field_name is invalid.')
            # Append field to field_names_lst to account for duplicate fields.
            elif field not in field_names_lst:
                field_names_lst.append(field)

    elif type(field_names) is str:
        if len(field_names) > 1:
            if ',' in field_names:
                # If a comma is present in field_names, split each field in field_names at the comma.
                field_names = field_names.split(",")
                # Remove unnecessary spaces from each field.
                field_names = [field.strip() for field in field_names]
                for field in field_names:
                    if field in keyword.kwlist or not field[0].isalpha():
                        raise SyntaxError(field_names)
                    elif field not in field_names_lst:
                        field_names_lst.append(field)
            else:
                # If only spaces are present in field names, split each field at the space.
                field_names = field_names.split(" ")
                field_names = [field for field in field_names if field.strip()]

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

    # __init__ method
    init_field_strings = ""
    for field in field_names_lst:
        init_field_strings += "self." + field + " = " + field + "\n" + "        "

    init_param_strings = ""
    for field in field_names_lst:
        if field in defaults:
            init_param_strings += field + " = " + str(defaults[field]) + ", "
        else:
            init_param_strings += field + ", "
    # Slice init_param_strings to account for extra spaces and/or commas.
    init_param_strings = init_param_strings[:-2]

    init_final_str = "class " + type_name + ":" + "\n"\
                     + "    " + "_fields = " + str(field_names) + "\n"\
                     + "    " + "_mutable = " + str(mutable) + "\n"\
                     + "    " + "def __init__(self, " + init_param_strings + "):\n"\
                     + "        " + init_field_strings + "\n"

    # __repr__ method
    repr_param_str = ""
    for field in field_names_lst:
        # Format example: x = self.x
        repr_param_str += f"{field}={{self.{field}}},"
    # Slice repr_param_str to account for extra spaces/comma.
    repr_param_str = repr_param_str[:-1]

    repr_final_str = ""
    repr_final_str += "    " + "def __repr__(self):\n"\
                      + f"        return f'{type_name}({repr_param_str})'\n"

    # query/accessor methods
    accessor_final_str = ""
    for field in field_names_lst:
        accessor_final_str += "    " + "def get_" + field + "(self):\n"\
                              + "        " + "return self." + field + "\n"

    # __getitem__ method
    indexing_final_str = ""
    indexing_final_str += "    " + "def __getitem__(self, index):\n"\
                          + "        " + "if type(index) is int:\n"\
                          + "            " + "return getattr(self, self._fields[index])\n"\
                          + "        " + "else:\n"\
                          + "            " + "raise TypeError\n"

    # __eq__ method
    eq_final_str = ""
    eq_final_str += "    " + "def __eq__(self, other):\n"\
                    + "        " + ("if type(self) == type(other) " 
                                    "and self.__dict__ == other.__dict__:") + "\n"\
                    + "            " + "return True\n"\
                    + "        " + "else:\n"\
                    + "            " + "return False\n"

    # _asdict method
    as_dict_final_str = ""
    as_dict_final_str += "    " + "def _asdict(self):\n"\
                         + "        " + "return self.__dict__\n"

    make_method_str = ""
    make_method_str += "    " + "def _make(iterable):\n"\
                       + "        " + "if len(iterable) != len(" + type_name + "._fields):\n"\
                       + "          " + "raise ValueError('iterable length does not match _fields length')\n"\
                       + "        " + "else:\n"\
                       + "          " + "# Unpack the iterable's contents.\n"\
                       + "          " + "return " + type_name + "(*iterable)\n"

    # _replace method
    replace_method_str = ""
    replace_method_str += "    " + "def _replace(self, **kargs):\n"\
                          + "        " + "if not kargs:\n"\
                          + "            " + "raise TypeError('kargs cannot be empty')\n"\
                          + "        " + "if self._mutable:\n"\
                          + "          " + "for key in kargs:\n"\
                          + "              " + "if key in self.__dict__:\n"\
                          + "                  " + "# Update self.__dict__ with the content of kargs.\n"\
                          + "                  " + "self.__dict__[key] = kargs[key]\n"\
                          + "              " + "else:\n"\
                          + "                  " + "raise TypeError\n"\
                          + "          " + "return None\n"\
                          + "        " + "else:\n"\
                          + "          " + "current_dict = {field: value for field, value in self.__dict__.items()}\n"\
                          + "          " + "for key in kargs:\n"\
                          + "              " + "if key in current_dict:\n"\
                          + "                  " + "current_dict[key] = kargs[key]\n"\
                          + "          " + "# Unpack the dictionary's contents.\n"\
                          + "          " + "return " + type_name + "(**current_dict)\n"


    # __setattr__ method
    set_attr_method_str = ""
    set_attr_method_str += "    " + "def __setattr__(self, name, value):\n"\
                           + "        " + "if name in self._fields:\n"\
                           + "            " + "if self._mutable:\n"\
                           + "                " + "self.__dict__[name] = value\n"\
                           + "            " + "elif name not in self.__dict__:\n"\
                           + "                " + "self.__dict__[name] = value\n"\
                           + "            " + "else:\n"\
                           + "                " + "raise AttributeError('Cannot change attributes.')\n"\
                           + "        " + "else:\n"\
                           + "            " + "raise AttributeError('Cannot add new attributes.')\n"

    final_str = (init_final_str + repr_final_str + accessor_final_str + indexing_final_str + eq_final_str +
                 as_dict_final_str + make_method_str + replace_method_str + set_attr_method_str)

    exec(final_str, locals())
    return locals().get(type_name)
