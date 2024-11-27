# A simple generator function

def my_gen():
    n = 1
    print('Primeiro print, n é igual a {}'.format(n))
    # Generator function contains yield statements
    yield n

    n += 1
    print('Segundo print, n é igual a {}'.format(n))
    yield n

    n+= 1
    print('Terceiro print, n é igual a {}'.format(n))
    yield n