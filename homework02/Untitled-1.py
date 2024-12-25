DICT_1 = {"a": 1, "b": 2}
DICT_2 = {"a": 3, "c": 4}


def func(dict_1, dict_2):
    dict_1.update(dict_2)
    return dict_1

print(func(DICT_1, DICT_2))
