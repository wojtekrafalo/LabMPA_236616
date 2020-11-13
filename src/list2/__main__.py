from src.list2.analysis_extendable import *
from src.list2.perm_impl import *
from src.list2.test import *


def main():
    # print("\nPermutation analysis:")
    # print_analysis(generate_random_perm, "csv/perm.csv", "csv/perm_hist.csv")
    # print_random_perms()

    constants = Constants(
        n_max=1_000,
        n_min=50,
        step=10,
        reps=200,
        hist_reps=1_000,
        hist_n=1_000,
        cheb_prob=0.8
    )

    f_const = RandomVariableData(count_constants, theoretical_ex_val_for_n, theoretical_variance_for_n, "csv/const.csv",
                                 "csv/const_hist.csv")
    f_cyc = RandomVariableData(count_cycles, theoretical_ex_val_for_n, theoretical_variance_for_n, "csv/cyc.csv",
                               "csv/cyc_hist.csv")
    f_rec = RandomVariableData(count_records, theoretical_ex_val_for_n, theoretical_variance_for_n, "csv/rec.csv",
                               "csv/rec_hist.csv")
    print("\nConsts analysis:")
    print_analysis(f_const, constants)
    print("\nCycles analysis:")
    print_analysis(f_cyc, constants)
    print("\nRecords analysis:")
    print_analysis(f_rec, constants)


if __name__ == '__main__':
    main()
