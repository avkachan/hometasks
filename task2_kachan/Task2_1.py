key = ['one', 'two', 'three', 'four', 'five']
val = [1, 2, 3, 4]


def create_dict(key, val):
    if len(key) > len(val):
        while len(key) > len(val):
            val.append(None)
    else:
        val = val[0:len(key)]
    return {key: value for key, value in zip(key, val)}


print(create_dict(key, val))
