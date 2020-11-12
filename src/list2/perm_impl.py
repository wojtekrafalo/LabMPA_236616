# import random
from numpy import random


def theoretical_ex_val_for_n(n, fun):
    if fun == count_constants:
        return 1
    elif fun == count_cycles:
        return count_harmonic(n)
    elif fun == count_records:
        return count_harmonic(n)


def theoretical_variance_for_n(n, fun):
    if fun == count_constants:
        return 1
    elif fun == count_cycles:
        return count_variance(n)
    elif fun == count_records:
        return count_variance(n)


def count_variance(n):
    har = [0]
    for i in range(1, n + 1):
        har.append(har[i - 1] + (1.0 / float(i)))
    var = 0
    for i in range(1, n):
        var += har[i] / float(i + 1)
    var *= 2
    var += har[n]
    var -= (har[n] * har[n])
    return var


def generate_random_perm(n):
    a = random.permutation(n)
    return a


def print_perm(perm):
    print("[", end="")
    for i in perm:
        print(i, end="")
    print("]")


def count_constants(perm):
    num = 0
    for i in perm:
        if perm[i] == i:
            num += 1
    return num


def count_cycles(perm):
    not_visited = 0
    paint = 1
    size = perm.__len__()
    arr = [not_visited] * size

    it = 0
    traveler = 0
    while it < size:
        if arr[traveler] == 0:
            arr[traveler] = paint
            traveler = perm[traveler]
        elif arr[traveler] < paint:
            it += 1
            traveler = it
        elif arr[traveler] == paint:
            paint += 1
            it += 1
            traveler = it

    return paint - 1


def count_records(perm):
    num_rec = 0
    max_element = -1

    for e in perm:
        if e > max_element:
            max_element = e
            num_rec += 1
    return num_rec


def count_harmonic(n):
    har = 0
    for i in range(1, n+1):
        har += 1.0/float(i)
    return har


# code below is deprecated
def generate_rand_perm_traditional(n):
    perm = []

    helper = [False] * n
    # for _ in range(0, n):
    #     helper.append(False)

    for i in range(0, n):
        p = get_random_index(n - i)
        helper[p] = True

        idx = 0
        i_app = 0
        while idx < p:
            if helper[idx]:
                i_app += 1
            idx += 1

        perm.append(i_app)
    return perm


def get_random_index(n):
    return random.randint(0, n - 1)
