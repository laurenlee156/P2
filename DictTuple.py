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
            print(dictionary)
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
            self.dt[0].append({k: v})
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

    #def __call__(self, *args, **kwargs):



#o = DictTuple({'a': 1, 'b': 2, 'c': 3}, {'c': 13, 'd': 14, 'e': 15})
# #d = DictTuple([{'a': 2, 'b': 3, 'c': 4}])
#print(o)
#print(o.__len__())
# print(o.__bool__())
# # print(o.__repr__())
# #print(o.__contains__('c'))
# #print(o.__getitem__('c'))
# #print(d.__contains__('a'))
# print(o.__setitem__('adf', 2))
#print(o.__delitem__('a'))