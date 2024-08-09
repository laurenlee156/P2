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

# o = DictTuple({'c1': 2}, {'c1': 3})
# print(o.__bool__())
# print(o.__repr__())
# print(o.__contains__('c2'))