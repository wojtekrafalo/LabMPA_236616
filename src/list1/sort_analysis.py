import math
from math import sqrt, ceil

from src.list1.merge_sort_impl import my_merge_sort
from src.list1.quick_sort_impl import my_quick_sort
import random


N_MAX = 2000
N_MIN = 50
STEP = 50
REPS = 200
HIST_REPS = 20_000
HIST_N = 1000
CHEB_PROB = 0.8
I_MIN = -100_000
I_MAX = 100_000


# N_MAX = 500
# N_MIN = 50
# STEP = 50
# REPS = 150
# HIST_REPS = 6_000
# HIST_N = 500
# CZEB_PROB = 0.8
# I_MIN = -100_000
# I_MAX = 100_000


class DataAnalysis:
    def __init__(self, n, es_ex_max, es_ex_min, es_ex_avg, es_var, teo_ex, teo_var, czeb_width):
        self.n = n
        self.es_ex_max = es_ex_max
        self.es_ex_min = es_ex_min
        self.es_ex_avg = es_ex_avg
        self.es_var = es_var
        self.teo_ex = teo_ex
        self.teo_var = teo_var
        self.czeb = czeb_width

    def __str__(self):
        return str(self.n) + ", " + str(self.es_ex_max) + ", " + str(self.es_ex_min) + ", " + str(
            self.es_ex_avg) + ", " + str(self.es_var) + ", " + str(self.teo_ex) + ", " + str(self.teo_var) + ", " + str(
            self.teo_ex + self.czeb) + ", " + str(
            self.teo_ex - self.czeb)


def print_array(arr):
    ret = "n, es_ex_max, es_ex_min, es_ex_avg, es_var, teo_ex, teo_var, teo_ex + czeb, teo_ex - czeb\n"
    for w in arr:
        ret += w.__str__() + "\n"
    return ret


def collect_data(fun):
    data_list = []
    for n in range(N_MIN, N_MAX, STEP):
        es_ex_max, es_ex_min, es_ex_avg, es_var = estimate_ex_val_and_variance_for_n(n, fun)
        teo_ex = theoretical_ex_val_for_n(n, fun)
        teo_var = theoretical_variance_for_n(n, fun)
        if fun == my_merge_sort:
            teo_var = es_var
        cheb_width = chebyshev_width(teo_var, CHEB_PROB)

        data_list.append(
            DataAnalysis(n, es_ex_max, es_ex_min, es_ex_avg, es_var, teo_ex, teo_var, cheb_width))

    print("First phase of analysis of algorithm completed")
    hist = find_histogram(fun)
    return data_list, hist


def theoretical_ex_val_for_n(n, fun):
    out = 0
    gamma = 0.57721

    if fun == my_quick_sort:
        out = 2 * (n + 1) * (
                gamma + math.log(n) + (1 / (2 * n)) - (1 / (12 * n * n)) + (1 / (120 * n * n * n * n))) - 4 * n
        return out

    elif fun == my_merge_sort:
        return (n * math.log(n, 2)) - n + 1


def recursive_merge_comparisons(n):
    if n == 1:
        return 1
    if n == 0:
        return 0
    else:
        return 2 * recursive_merge_comparisons(math.ceil(float(float(n) / 2.0))) + n


def theoretical_variance_for_n(n, fun):
    if fun == my_quick_sort:
        var = 7 * n * n + 13 * n
        h_n = 0
        h_n_2 = 0
        for i in range(1, n + 1):
            h_n += 1 / i
            h_n_2 += 1 / (i * i)
        var -= 4 * (n + 1) * (n + 1) * h_n_2
        var -= 2 * (n + 1) * h_n
        return var
    else:
        return 0


def estimate_ex_val_and_variance_for_n(n, fun):
    max_c = 0
    min_c = 2_000_000_000
    sum_c = 0
    var = 0
    var_values = []

    for i in range(0, REPS):
        num = sort_random_table(n, fun)
        if num > max_c:
            max_c = num
        if num < min_c:
            min_c = num
        sum_c += num
        var_values.append(num)

    ex_val = float(float(sum_c) / float(REPS))
    for v in var_values:
        var += math.pow(v - ex_val, 2)
    var /= REPS
    return max_c, min_c, ex_val, var


def find_histogram(fun):
    hist_values = {}
    hist_ex = 0
    for i in range(0, HIST_REPS):
        num = sort_random_table(HIST_N, fun)
        hist_ex += num
        if hist_values.__contains__(num):
            hist_values[num] = hist_values[num] + 1
        else:
            hist_values[num] = 1
    return hist_values


def sort_random_table(n, fun):
    table = []
    random.seed()
    for _ in range(0, n):
        table.append(random.random())
    tab, num = fun(table)
    check_sorted(tab)
    return num


def check_sorted(table):
    for i in range(1, len(table)):
        if table[i] < table[i - 1]:
            raise ArithmeticError("Bad sorting!")
    return True


def chebyshev_width(var, p):
    return sqrt(abs(var / p))


def count_chebyshev_for_kurtosis(hist):
    ex = 0
    var = 0
    num_cheb = 0
    for i in hist:
        ex += i * hist[i]
        var += i * i * hist[i]
    ex = ex / HIST_REPS
    var = var - (ex * ex)

    for i in hist:
        if abs(ex - i) <= chebyshev_width(var, CHEB_PROB):
            num_cheb += hist[i]
    return num_cheb / HIST_REPS, ex, chebyshev_width(var, CHEB_PROB)


def print_analysis(fun, file_name, hist_file_name):
    data, hist = collect_data(fun)
    file = open(file_name, "w")
    file.write(print_array(data))
    file.close()

    percent_of_emp, hist_ex, cheb_width = count_chebyshev_for_kurtosis(hist)
    print_hist_values(hist, hist_ex, percent_of_emp, cheb_width, hist_file_name)
    print("Whole analysis of algorithm completed")


def print_hist_values(hist, hist_ex, percent_of_emp, cheb_width, file_name):
    file = open(file_name, "w")
    is_first = True
    for i in hist:
        file.write(i.__str__())
        file.write(",")
        file.write(hist[i].__str__())
        if is_first:
            file.write(", " + hist_ex.__str__())
            file.write(", " + percent_of_emp.__str__())
            file.write(", " + cheb_width.__str__())
            is_first = False
        file.write("\n")
    file.close()
