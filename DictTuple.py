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
            for key in dictionary:
                if key not in distinct_key_lst:
                    distinct_key_lst.append(key)
        return sorted(distinct_key_lst)

    # def __eq__(self, other):
    #     print(self.dt)
    #
    #     keys_lst = []
    #     first_lst = [(key, value) for dictionary in self.dt for key, value in dictionary.items()]
    #     # for dictionary in self.dt:
    #     #     for key in dictionary:
    #     #         keys_lst.append(key)
    #     # print(keys_lst)
    #     print('first list', first_lst)
    #     print(type(other))
    #     if isinstance(other, DictTuple):
    #         other = list(other)



        # first_lst = [(key, value) for dictionary in self.dt for key, value in dictionary.items()]
        # #print(first_lst)
        #
        # second_lst = [(key, value) for arg in list(other) for key, value in arg.items() if isinstance(arg, dict)]
        # if first_lst == second_lst:
        #     return True
        # return False



    def __add__(self, other):
        lst_of_dt = []
        for dictionary in self.dt:
            lst_of_dt.append(dictionary)
        for dictionary in other.dt:
            lst_of_dt.append(dictionary)

        return DictTuple({key: value for dictionary in lst_of_dt for key, value in dictionary.items()})

# o = DictTuple({'a': 1, 'b': 2, 'c': 3}, {'c': 13, 'd': 14, 'e': 15})
# #d = DictTuple([{'a': 2, 'b': 3, 'c': 4}])
# #print(o)
# d1 = DictTuple({'c1': (1, 2)}, {'c1': (3, 4)})
# d2 = DictTuple({'c2': (1, 2)}, {'c3': (3, 4)})
# print(d1 + d2)
#print(o.__eq__([('a', 1), ('b', 2), ('b', 12), ('c', 13)]))
#print(o.__eq__(DictTuple({'a': 1, 'b': 2, 'c': 3}, {'c': 13, 'd': 14, 'e': 15})))

#print(o.__len__())
#print(o.__iter__())
#print(d.__call__('g'))
# print(o.__bool__())
# # print(o.__repr__())
# #print(o.__contains__('c'))
# #print(o.__getitem__('c'))
# #print(d.__contains__('a'))
#print(o.__setitem__('adf', 2))
#print(o.__delitem__('a'))