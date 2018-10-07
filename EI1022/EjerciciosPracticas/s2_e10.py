def generador(iter):
    for elem in iter:
        yield elem * elem


for elem in generador([1, 2, 10, 4, 5]):
    print(elem)