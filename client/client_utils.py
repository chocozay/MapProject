
def is_tuple(tuple_str):
    if isinstance(eval(tuple_str), tuple) and len(eval(tuple_str)) == 2:
        return eval(tuple_str)
