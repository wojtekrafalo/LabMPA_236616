import math

NUM_Q = 0


def my_quick_sort(table):
    global NUM_Q
    NUM_Q = 0
    quick_sort_alg(table, 0, len(table) - 1)
    return table, NUM_Q


def quick_sort_alg(table, i_start, i_end):
    pivot = table[i_end]
    i_pivot = i_start
    num_p = 0

    i = i_start
    while i < i_end:
        num_p += 1
        if compare(table[i], pivot):
            swap(table, i, i_pivot)
            i_pivot += 1
        i += 1
    swap(table, i_end, i_pivot)

    if i_start < i_pivot - 1:
        quick_sort_alg(table, i_start, i_pivot - 1)
    if i_pivot + 1 < i_end:
        quick_sort_alg(table, i_pivot + 1, i_end)


def swap(tab, i, j):
    temp = tab[i]
    tab[i] = tab[j]
    tab[j] = temp


def compare(a, b):
    global NUM_Q
    NUM_Q += 1
    return a < b
