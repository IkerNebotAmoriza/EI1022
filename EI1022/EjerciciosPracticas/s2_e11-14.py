def first(n, iter):
    for elem in iter:
        if n == 0:
            break
        yield elem
        n -= 1


def filter(f, iter):
    for elem in iter:
        if f(elem):
            yield elem


def take_while(f, iter):
    for elem in iter:
        if not f(elem): break
        yield elem


def squares():
    n = 1
    while (True):
        yield n * n
        n += 1


def escapicua(n):
    a = str(n)
    b = a[::-1]
    return a == b


a = first(100, squares())
print(list(a))

b = take_while(lambda n: n < 100, squares())
print(list(b))

c = first(20, filter(escapicua, squares()))
print(list(c))