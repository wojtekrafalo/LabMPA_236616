NUM_M = 0


def my_merge_sort(table):
    global NUM_M
    NUM_M = 0
    return merge_sort_alg(table), NUM_M


def merge_sort_alg(table):
    if len(table) == 1:
        return table

    separator = int((0 + len(table)) / 2)
    list_smaller = merge_sort_alg(table[0:separator])
    list_bigger = merge_sort_alg(table[separator:len(table)])

    merged_table = merge(list_smaller, list_bigger, table)
    return merged_table


def merge(table_left, table_right, table):

    i = j = k = 0
    num_comp = 0
    while i < len(table_left) and j < len(table_right):
        if compare(table_left, table_right, i, j):
            table[k] = table_left[i]
            i += 1
        else:
            table[k] = table_right[j]
            j += 1
        k += 1
        num_comp += 1

    while i < len(table_left):
        table[k] = table_left[i]
        i += 1
        k += 1

    while j < len(table_right):
        table[k] = table_right[j]
        j += 1
        k += 1
    return table


def compare(list_first, list_second, i, j):
    len_first = len(list_first)
    len_second = len(list_second)

    if i >= len_first and j >= len_second:
        raise ValueError("Wrong algorithm")
    if i > len_first or j > len_second:
        raise ValueError("Wrong algorithm")

    global NUM_M
    NUM_M += 1

    if i >= len_first:
        return False
    if j >= len_second:
        return True
    return list_first[i] < list_second[j]
