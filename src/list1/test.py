from src.list1.merge_sort_impl import my_merge_sort
from src.list1.quick_sort_impl import my_quick_sort, quick_sort_4
from src.list1.sort_analysis import *


def test_merge_expected_values():
    print(recursive_merge_comparisons(2000))
    print(theoretical_ex_val_for_n(2000, my_merge_sort))


def test_quick():
    a = [9, -3, 5, 2, 6, 8, -6, 1, 3]
    my_quick_sort(a)
    print(a)


def test_output():
    num_comparisons = sort_random_table(50, my_merge_sort)
    print(num_comparisons)
    num_comparisons = sort_random_table(50, my_merge_sort)
    print(num_comparisons)


def test_4():
    array = [29, 99, 27, 41, 66, 28, 44, 78, 87, 19, 31, 76, 58, 88, 83, 97, 12, 21, 44]

    p = quick_sort_4(array, 0, len(array) - 1)
    print(array)
    print(p)


    array = [29, 99, 27, 41, 66, 28, 44, 78, 87, 19, 31, 76, 58, 88, 83, 97, 12, 21, 44]
    p = my_quick_sort(array)
    print(array)
    print(p)


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


def merge_ex_val_test():
    it = 0
    i = 1
    n = 2048
    equation = n + (n * math.log(n, 2))

    while i <= n:
        comp = ceil(n / i)
        it += comp * (i - 1)
        i *= 2

    print("iterative:" + it.__str__())
    print("quation:" + equation.__str__())
    return it, equation


def main():
    # test_4()
    merge_ex_val_test()


if __name__ == '__main__':
    main()
