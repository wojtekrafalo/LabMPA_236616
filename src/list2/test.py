from src.list2.perm_impl import get_random_index, generate_rand_perm_traditional, generate_random_perm, print_perm


def hist_test():
    hist_values = {}
    hist_values[8] = 8
    hist_values[3] = 12
    hist_values[9] = 2
    print(hist_values)

    if hist_values.__contains__(8):
        print("CONTAINS!")

    for a in hist_values:
        print("idx: " + a.__str__())
        print("val: " + hist_values[a].__str__())


def test_range():
    h_n = 0
    for i in range(1, 4):
        h_n += 1/i
        print(i)

    print(h_n)


def main():
    # test_4()
    test_range()
    print(count_h_n(10_000))


def print_random():
    for _ in range(0, 100):
        print(get_random_index(10))


def print_random_perms():
    for _ in range(0, 100):
        print(generate_rand_perm_traditional(10))


def print_random_perms_numpy():
    for _ in range(0, 100):
        print_perm(generate_random_perm(10))


def count_h_n(n):
    ex = 0
    for i in range(1, n + 1):
        ex += 1.0 / float(i)
    return ex


if __name__ == '__main__':
    main()
