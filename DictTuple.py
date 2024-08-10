class DictTuple:
    def __init__(self, *args):
        if len(args) == 0:
            raise AssertionError("DictTuple.__init__: There must be at least one dictionary.")
        for arg in args:
            #print(arg)
            if type(arg) is not dict:
                raise AssertionError("DictTuple.__init__: Each argument must be a dictionary.")
            if len(arg) == 0:
                raise AssertionError("DictTuple.__init__: Dictionary cannot be empty")

        self.dt = list(args)
        #print(self.dt)

    # count number of distinct keys
    def __len__(self):
        distinct_key_lst = []

        for dictionary in self.dt:
            for key in dictionary:
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
        return False

    def __getitem__(self, k):
        if not self.__contains__(k):
            raise KeyError("Key does not exist.")

        for dictionary in reversed(self.dt):
            if k in dictionary:
                return dictionary[k]
    def __setitem__(self, k, v):
        if not self.__contains__(k):
            self.dt.append({k: v})
            return self.dt

        for dictionary in reversed(self.dt):
            if k in dictionary:
                dictionary[k] = v
        return self.dt

    def __delitem__(self, k):
        if not self.__contains__(k):
            raise KeyError("Key does not exist.")

        for dictionary in self.dt:
            dictionary.pop(k, None)
        return self.dt

    def __call__(self, k):
        values_lst = []
        if not self.__contains__(k):
            return []

        for dictionary in self.dt:
            if k in dictionary:
                values_lst.append(list(dictionary.values()))

        return values_lst

    def __iter__(self):
        distinct_key_lst = []

        for dictionary in reversed(self.dt):
            for key in sorted(dictionary):
                if key not in distinct_key_lst:
                    distinct_key_lst.append(key)
        return iter(distinct_key_lst)

    def __eq__(self, other):
        # other.dt is a list of dictionaries
        if type(other) is DictTuple:
            return self.dt == other.dt
        else:
            dict_tuple = [other]
            return self.dt == dict_tuple

    def __add__(self, other):
        lst_of_dt = []
        for dictionary in self.dt:
            lst_of_dt.append(dictionary)
        for dictionary in other.dt:
            lst_of_dt.append(dictionary)

        return DictTuple({key: value for dictionary in lst_of_dt for key, value in dictionary.items()})

#o = DictTuple({'a': 1, 'b': 2, 'c': 3}, {'c': 13, 'd': 14, 'e': 15})
# #d = DictTuple([{'a': 2, 'b': 3, 'c': 4}])
# #print(o)
#d1 = DictTuple({'c1': (1, 2)}, {'c1': (3, 4)})
#d2 = DictTuple({'c2': (1, 2)}, {'c3': (3, 4)})
#print(d1 + d2)
#print(o.__eq__([('a', 1), ('b', 2), ('b', 12), ('c', 13)]))
#print(o.__eq__(DictTuple({'a': 1, 'b': 2, 'c': 3}, {'c': 13, 'd': 14, 'e': 15})))

# c = DictTuple({'a': 1, 'b': 2}, {'b': 12, 'c': 13})
# d = DictTuple({'a': 1, 'b': 12}, {'c': 13})
# #
# print(c.__eq__(d))
#
# f = DictTuple({'b': 1, 'a': 2}, {'e': 12, 'f': 13})
# print(f.__iter__())
