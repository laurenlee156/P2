import keyword

# compute a large string that describes the class, and return the class object it represents
def mynamedtuple(type_name, field_names, mutable = False, defaults = {}):
    # checks if any part of type_name is a Python keyword
    if type_name in keyword.kwlist:
        raise SyntaxError('type_name cannot be a Python keyword.')
    # check the type of type_name
    elif type(type_name) is not str:
        raise SyntaxError('type_name must be a string.')
    # checks if the first character of type_name is a letter
    elif not type_name.strip() or not type_name.strip()[0].isalpha():
        raise SyntaxError('type_name must begin with a letter.')

    field_names_lst = []
    if type(field_names) is list:
        for field in field_names:
            if field in keyword.kwlist or not field[0].isalpha() or field in field_names_lst:
                raise SyntaxError('field_name is invalid.')
            elif field not in field_names_lst:
                field_names_lst.append(field)

    elif type(field_names) is str:
        if len(field_names) > 1:
            if ',' in field_names:
                field_names = field_names.split(",")
                field_names = [field.strip() for field in field_names]

                for field in field_names:
                    if field in keyword.kwlist or not field[0].isalpha() or field in field_names_lst:
                        raise SyntaxError('field_name is invalid.')
                    elif field not in field_names_lst:
                        field_names_lst.append(field)
            else:
                field_names = field_names.split(" ")
                field_names = [field for field in field_names if field.strip()]

                for field in field_names:
                    if field in keyword.kwlist or not field[0].isalpha() or field in field_names_lst:
                        raise SyntaxError('field_name is invalid.')
                    elif field not in field_names_lst:
                        field_names_lst.append(field)
        elif len(field_names) == 0:
            raise SyntaxError('field_names is empty.')
        else:
            if field_names in keyword.kwlist or not field_names[0].isalpha() or field_names in field_names_lst:
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
                     + "        " + "self._mutable = True" + "\n"\
                     + "        " + init_field_strings + "\n"\
                     + "        " + "self._mutable = " + str(mutable) + "\n"

    # repr method
    repr_param_str = ""
    for field in field_names_lst:
        repr_param_str += f"{field}={{self.{field}}},"
    repr_param_str = repr_param_str[:-1]

    repr_final_str = ""
    repr_final_str += "    " + "def __repr__(self):\n"\
                      f"        return f'{type_name}({repr_param_str})'\n"

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
                       + "        " + "if len(iterable) != len(" + type_name + "._fields):" + "\n"\
                       + "          " + "raise ValueError('iterable length does not match _fields length')" + "\n"\
                       + "        " + "else:" + "\n"\
                       + "          " + "return " + type_name + "(*iterable)" + "\n"

    # _replace method
    replace_method_str = ""
    replace_method_str += "    " + "def _replace(self, **kargs):" + "\n" \
                          + "        " + "if not kargs:" + "\n" \
                          + "            " + "raise TypeError('kargs cannot be empty')" + "\n" \
                          + "        " + "if self._mutable:" + "\n"\
                          + "          " + "for key in kargs:" + "\n"\
                          + "              " + "if key in self.__dict__:" + "\n"\
                          + "                  " + "self.__dict__[key] = kargs[key]" + "\n"\
                          + "              " + "else:" + "\n"\
                          + "                  " + "raise TypeError" + "\n"\
                          + "          " + "return None" + "\n"\
                          + "        " + "else:" + "\n"\
                          + "          " + "current_dict = {field: value for field, value in self.__dict__.items()}" + "\n"\
                          + "          " + "for key in kargs:" + "\n"\
                          + "              " + "if key in current_dict:" + "\n"\
                          + "                  " + "current_dict[key] = kargs[key]" + "\n"\
                          + "          " + "return " + type_name + "(**current_dict)" + "\n"


    # __setattr__ method
    set_attr_method_str = ""
    set_attr_method_str += "    " + "def __setattr__(self, name, value):" + "\n"\
                           + "        " + "if self._mutable == False:" + "\n"\
                           + "            " + "raise AttributeError('Cannot change attributes.')" + "\n"\
                           + "        " + "else:" "\n"\
                           + "            " + "self.__dict__[name] = value" + "\n"

    final_str = init_final_str + repr_final_str + accessor_final_str + indexing_final_str + eq_final_str + as_dict_final_str + make_method_str + replace_method_str + set_attr_method_str
    #print(final_str)
    exec(final_str, locals())
    return locals().get(type_name)

#coord = mynamedtuple("coordinate", "x y", mutable = False)
#c = coord(0, 0)
#c.__setattr__("x", 1)
# # #c.attr2 = coord(1, 0)
# #
#print(c)

