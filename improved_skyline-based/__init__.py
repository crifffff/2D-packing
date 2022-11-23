from improved_skyline_based import *


def main():
    # 给定相关值或者读取相关值
    w = 100
    all_items = [[30, 20], [15, 27], [13, 21], [50, 26], [39, 49], [15, 38], [13, 15],
                 [29, 67], [9, 17], [20, 57], [39, 27]]

    # all_items = [[30, 20], [15, 27], [13, 21], [50, 26], [39, 49]]

    improved = ImprovedSkylineBased(all_items, w)

    improved.packing()


if __name__ == '__main__':
    main()
