def float_range(start, end, step):
    x = start
    while x < end:
        yield x
        x += step

def normalize(x, min, max, value_range = None):
    if value_range == None:
        return (x - min) / (max - min)
    else:
        return (x - min) / value_range

def integral(func, a, b, dx, **kwargs):
    result = 0
    
    for x in float_range(a, b, dx):
        result += func(x, **kwargs) * dx
    
    return result

def float_str(x):
    return "{0:.2f}".format(x)