import math

from src.list2.perm_impl import generate_random_perm


# N_MAX = 2000
# N_MIN = 50
# STEP = 50
# REPS = 200
# HIST_REPS = 20_000
# HIST_N = 1000
# CHEB_PROB = 0.8
# I_MIN = -100_000
# I_MAX = 100_000
EPS = 0.0000001

def print_analysis(functions, constants):
    data, hist = collect_data(functions.fun, functions.theo_ex_fun, functions.theo_var_fun, constants)
    file = open(functions.file, "w")
    file.write(print_array(data))
    file.close()

    percent_of_emp, hist_ex, cheb_width = count_chebyshev_for_kurtosis(hist, constants.HIST_REPS, constants.CHEB_PROB)
    print_hist_values(hist, hist_ex, percent_of_emp, cheb_width, functions.hist_file)
    print("Whole analysis of algorithm completed")


class Constants:
    def __init__(self, n_max, n_min, step, reps, hist_reps, hist_n, cheb_prob):
        self.N_MAX = n_max
        self.N_MIN = n_min
        self.STEP = step
        self.REPS = reps
        self.HIST_REPS = hist_reps
        self.HIST_N = hist_n
        self.CHEB_PROB = cheb_prob


class RandomVariableData:
    def __init__(self, fun, theo_ex_fun, theo_var_fun, file, hist_file):
        self.fun = fun
        self.theo_ex_fun = theo_ex_fun
        self.theo_var_fun = theo_var_fun
        self.file = file
        self.hist_file = hist_file


class DataAnalysis:
    def __init__(self, n, p_max, p_min, es_ex, es_var, teo_ex, teo_var, cheb_width):
        self.n = n
        self.max = p_max
        self.min = p_min
        self.es_ex = es_ex
        self.es_var = es_var
        self.teo_ex = teo_ex
        self.teo_var = teo_var
        self.cheb = cheb_width

    def __str__(self):
        return str(self.n) + ", " + str(self.max) + ", " + str(self.min) + ", " + str(
            self.es_ex) + ", " + str(self.es_var) + ", " + str(self.teo_ex) + ", " + str(self.teo_var) + ", " + str(
            self.teo_ex + self.cheb) + ", " + str(
            self.teo_ex - self.cheb)


def print_array(arr):
    ret = "n, max, min, es_ex, es_var, teo_ex, teo_var, teo_ex + cheb, teo_ex - cheb\n"
    for w in arr:
        ret += w.__str__() + "\n"
    return ret


def collect_data(fun, theoretical_ex_fun, theoretical_var_fun, constants):
    data_comparisons = []
    for n in range(constants.N_MIN, constants.N_MAX, constants.STEP):
        es_max, es_min, es_ex, es_var = estimate_ex_val_and_variance_for_n(n, fun, constants.REPS)
        teo_ex = theoretical_ex_fun(n, fun)
        teo_var = theoretical_var_fun(n, fun)
        # czeb_width = chebyshev_width(teo_var, constants.CHEB_PROB)
        czeb_width = chernoff_width(teo_ex, constants.CHEB_PROB)

        data_comparisons.append(
            DataAnalysis(n, es_max, es_min, es_ex, es_var, teo_ex, teo_var, czeb_width))

    print("First phase of analysis of algorithm completed")
    hist = find_histogram(fun, constants.HIST_N, constants.HIST_REPS)
    return data_comparisons, hist


def print_hist_values(hist, hist_ex, percent_of_emp, cheb_width, file_name):
    file = open(file_name, "w")
    file.write("n, num, ex, percent_of_emp, cheb_width\n")
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


def count_chebyshev_for_kurtosis(hist, hist_reps, cheb_prob):
    ex = 0
    var = 0
    num_cheb = 0
    for i in hist:
        ex += i * hist[i]
        var += i * i * hist[i]
    ex = ex / hist_reps
    var = var - (ex * ex)

    for i in hist:
        # if abs(ex - i) <= chebyshev_width(var, cheb_prob):
        if abs(ex - i) <= chernoff_width(ex, cheb_prob):
            num_cheb += hist[i]
    # return num_cheb / hist_reps, ex, chebyshev_width(var, cheb_prob)
    return num_cheb / hist_reps, ex, chernoff_width(ex, cheb_prob)


def estimate_ex_val_and_variance_for_n(n, fun, reps):
    max_c = 0
    min_c = 2_000_000_000
    sum_c = 0
    var = 0
    var_values = []

    for i in range(0, reps):
        num = get_variable_value(n, fun)
        if num > max_c:
            max_c = num
        if num < min_c:
            min_c = num
        sum_c += num
        var_values.append(num)

    ex_val = float(float(sum_c) / float(reps))
    for v in var_values:
        var += math.pow(v - ex_val, 2)
    var /= reps
    return max_c, min_c, ex_val, var


def find_histogram(fun, hist_n, hist_reps):
    hist_values = {}
    hist_ex = 0
    for i in range(0, hist_reps):
        num = get_variable_value(hist_n, fun)
        hist_ex += num
        if hist_values.__contains__(num):
            hist_values[num] = hist_values[num] + 1
        else:
            hist_values[num] = 1
    return hist_values


def get_variable_value(n, fun):
    p = generate_random_perm(n)
    return fun(p)


def chebyshev_width(var, p):
    return math.sqrt(abs(var / p))


def chernoff_width(ex, p):
    a = 0
    b = 1
    delta = 0
    while chernoff_bisearch(b, p) - p > EPS:
        b *= 2

    while abs(b-a) > EPS:
        delta = (a+b)/2
        cher = chernoff_bisearch(delta, p)

        if abs(cher - ex) < EPS:
            break
        elif cher - p > EPS:
            a = delta
        else:
            b = delta
    return delta


def chernoff_bisearch(delta, p):
    return pow(pow(math.e, delta) / pow(1+delta, 1+delta), p)

