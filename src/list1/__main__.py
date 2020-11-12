from src.list1.merge_sort_impl import my_merge_sort
from src.list1.quick_sort_impl import my_quick_sort
from src.list1.sort_analysis import *


def main():
    print("\nQuickSort analysis:")
    print_analysis(my_quick_sort, "csv/quick.csv", "csv/quick_hist.csv")

    print("\nMergeSort analysis:")
    print_analysis(my_merge_sort, "csv/merge.csv", "csv/merge_hist.csv")


if __name__ == '__main__':
    main()
