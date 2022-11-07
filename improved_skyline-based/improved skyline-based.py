import heapq
import math
import bisect
from itertools import chain
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from gap import Gap
from DoubleLinkedList import DoubleLinkedList
from SegmentTree import SegmentTree


class ImprovedSkylineBased:
    def __init__(self, items, width):
        self.items = items
        self.width = width
        self.n = len(self.items)
        self.min_w = None

        self.R = None
        self.r1 = {}

        self.r2 = []
        self.r2_i = None
        self.r2_i_dict = {}
        self.tree2 = None

        self.r3 = []
        self.r3_i = None
        self.r3_i_dict = {}
        self.tree3 = None

        self.heap = None
        self.double_linked = None

        self.s_gap = None
        self.prior_s_gap, self.next_s_gap = None, None

        self.items_placed_i = 0
        self.items_placed = []
        self.fitness = None

        self.mid = None

    # R
    def init_R(self):
        new_item = []
        for (w, h) in self.items:
            new_item.append([h, w])
        a = list(chain.from_iterable(zip(self.items, new_item)))
        self.items = a
        return self.items

    # r1
    def init_r1(self):
        """
            将原R复制到r1中，并赋值一个key值，输出一个包含以下信息及特征的数据结构：
            包含key、i、w、h信息
            :param R: 原矩形列表 [[w, h], []]
            :return: 原矩形列表和包含k值的字典
            """

        for i, (w, h) in enumerate(self.R):
            k = self.key(w, h)
            # r1.setdefault(k, []).append(i)

            if k in self.r1:
                self.r1[k].append(i)
            else:
                self.r1[k] = [i]

    # r2函数(适用于已知一个w信息)
    def init_r2(self):
        """
           将R复制到r2中，输出一个包含以下信息及特征的数据结构
           1、按照w和i进行升序排列
           2、包含w，i，h信息
           :param R:原矩形列表
           :return:r2
           """

        for i, (w, h) in enumerate(self.R):
            self.r2.append([w, i, h])  # [[w, i, h]]
        self.r2.sort(reverse=False)

        self.r2_i = [self.r2[i][1] for i in range(len(self.r2))]
        for i in range(len(self.r2_i)):
            self.r2_i_dict[self.r2_i[i]] = i

        self.min_w = self.r2[0][0]

    # r3
    def init_r3(self):
        """
            将R复制到r3中，输出一个包含以下信息及特征的数据结构
            1、按照h和w进行升序排列
            2、包含w，i，h信息
            :param R:原矩形列表
            :return:r3
            """

        for i, (w, h) in enumerate(self.R):
            self.r3.append([h, w, i])  # [h, w, i]]
        self.r3.sort(reverse=False)

        self.r3_i = [self.r3[i][2] for i in range(len(self.r3))]
        for i in range(len(self.r3_i)):
            self.r3_i_dict[self.r3_i[i]] = i

    # tree2
    def init_tree2(self):
        self.tree2 = SegmentTree(self.r2_i)

    # tree3
    def init_tree3(self):
        self.tree3 = SegmentTree(self.r3_i)

    # 初始化items的辅助序列
    def init_items(self):

        self.R = self.init_R()
        self.init_r1()
        self.init_r2()
        self.init_r3()

        self.init_tree2()
        self.init_tree3()

    # 初始化gap的堆与双向链
    def init_gaps(self):
        gap = Gap(0, 0, self.width)
        self.heap = [gap]
        self.double_linked = DoubleLinkedList(self.width)
        self.double_linked.append(gap)

    # 初始化所有
    def init(self):
        self.init_items()

        self.init_gaps()

    # 是否有未安排的item
    def not_packed(self):
        return len(self.r2) > 0

    # lowest gap
    def find_lowest_gap(self):

        return heapq.heappop(self.heap)

    # lowest gap的前后gap
    def prior_next_gap(self):
        self.prior_s_gap = self.s_gap.prior
        self.next_s_gap = self.s_gap.next

    # 定义key值函数
    def key(self, w, h):
        a = h * (self.width + 1) + w
        return a

    # 确定item_palced_i,以及长宽
    def output_item(self):

        w, h = self.R[self.items_placed_i][0], self.R[self.items_placed_i][1]
        self.items_placed.append([w, h])

        return self.items_placed[-1]

    # 二分搜索找一个特定的值
    def binary_search_value(self, list_item, item, i):

        """
        找一个特定的值
        :param list_item:
        :param item:
        :return: 位置序列以及序列对应的值
        """
        low, high = 0, len(list_item) - 1

        while low < high:
            mid = int((low + high) / 2)
            if i >= 0:
                guess = list_item[mid][i]
            else:
                guess = list_item[mid]
            # 如果我们索引中的数字等于需要查找的目标，则程序结束，返回对应的索引，以及索引处对应的值
            if guess == item and list_item[mid - 1] != item:
                return mid
            else:
                high = mid - 1

            if guess > item:
                high = mid - 1

            else:
                low = mid + 1

        return None

    # 二分搜索法找一个有特定值的范围

    def binary_search_range_value(self, list_item, h, w):

        """
        在一个升序排列的列表中，找一个有一个特定值的最大范围
        :param list_item:
        :param h:
        :return: 一个范围的序列，以及对应的值
        """

        first = bisect.bisect(list_item, [h, 0, 0])
        if first <= len(list_item) - 1:
            if first >= 0:  # 表示至少存在一个item可以放进gap中
                if list_item[first] == h:
                    last = bisect.bisect(list_item, [h, w, 0]) - 1
                    return [self.r3_i_dict[list_item[first][2]], self.r3_i_dict[list_item[last][2]]]
        else:
            return None
        # low, high = 0, len(list_item) - 1
        #
        # while low < high:
        #     mid = int((low + high) / 2)
        #     guess1 = list_item[mid][i]
        #     # 如果我们索引中的数字等于需要查找的目标，则程序结束，返回对应的索引，以及索引处对应的值
        #     if guess1 == item:
        #         first, last = mid, mid
        #         while guess1 == item:
        #             first -= first
        #             guess1 = list_item[first][i]
        #         while guess1 == item:
        #             last += last
        #             guess1 = list_item[last][i]
        #         return first + 1, last - 1
        #
        #     if guess1 > item:
        #         high = mid - 1
        #
        #     else:
        #         low = mid + 1
        #
        # return None

    # 二分搜索法找一个无特定值的范围
    def binary_search_range(self, list_item, width, dict_item, i):

        """
        在一个升序排列的列表中，找一个不大于某个特定值的最大范围
        :param list_item:
        :param width:
        :return: 一个范围的序列，以及对应的值
        """
        index = bisect.bisect(list_item, [width, 0, 0])
        if index >= 1:  # 表示至少存在一个item可以放进gap中
            return dict_item[list_item[index - 1][i]]
        else:
            return -1
        # low, high = 0, len(list_item) - 1
        #
        # while low < high:
        #     mid = (low + high) // 2
        #     if list_item[mid][i] > width:
        #         high = mid
        #     else:
        #         low = mid + 1
        # index = low - 1
        # if index != -1:
        #     return index

        # mid = int((low + high) / 2)
        # guess1 = list_item[mid][i]
        # guess2 = list_item[mid + 1][i]
        # # 如果我们索引中的数字等于需要查找的目标，则程序结束，返回对应的索引，以及索引处对应的值
        # if (guess1 < item) and (guess2 > item):
        #     return list(range(mid + 1))
        #
        # if guess1 > item:
        #     high = mid - 1
        #
        # else:
        #     low = mid + 1

        # return None

    # 针对guess_key
    def find_specific_item(self, guess_key):
        if guess_key in self.r1:
            self.items_placed_i = self.r1[guess_key][0]
            item = self.output_item()
            return item

    # 找fitness==3的矩形
    def find_fitness3_item(self):
        if self.prior_s_gap.y == self.next_s_gap.y:
            guess_key = self.key(self.s_gap.w, self.prior_s_gap.y)
            item = self.find_specific_item(guess_key)
            return item

    # 找fitness==2的矩形
    def find_fitness2_item(self):
        if max(self.prior_s_gap.y, self.next_s_gap.y) != float("inf"):
            guess_key = self.key(self.s_gap.w, max(self.prior_s_gap.y, self.next_s_gap.y))
            item = self.find_specific_item(guess_key)
            if item is not None:
                return item
        else:
            guess_key = self.key(self.s_gap.w, min(self.prior_s_gap.y, self.next_s_gap.y))
            item = self.find_specific_item(guess_key)
            if item is not None:
                return item

        # if guess_key in self.r1:
        #     self.items_placed_i = self.r1[guess_key][0]
        #     item = self.output_item()
        #     self.fitness = 2
        #     return item
        # else:
        #     guess_key = self.key(self.s_gap.w, min(self.prior_s_gap.y, self.next_s_gap.y))
        #     if guess_key in self.r1:
        #         self.items_placed_i = self.r1[guess_key][0]
        #         item = self.output_item()
        #         self.fitness = 2
        #         return item
        #     else:
        #         return None

    # 找fitness==1的矩形
    def find_fitness1_item(self):
        # 找w
        a = self.binary_search_value(self.r2, self.s_gap.w, 0)

        if a is not None:
            self.items_placed_i = self.r2[a][1]
            item = self.output_item()
            self.fitness = 1
            return item
        else:
            if max(self.prior_s_gap.y, self.next_s_gap.y) != float("inf"):
                range = self.binary_search_range_value(self.r3, max(self.prior_s_gap.y, self.next_s_gap.y),
                                                       self.s_gap.w)
                if range is not None:
                    a, b = range[0], range[1]
                    self.items_placed_i, self.mid = self.tree3.query(a, b)
                    item = self.output_item()
                    self.fitness = 1
                    return item
                elif min(self.prior_s_gap.y, self.next_s_gap.y) != float("inf"):
                    range = self.binary_search_range_value(self.r3, min(self.prior_s_gap.y, self.next_s_gap.y),
                                                           self.s_gap.w)
                    if range is not None:
                        a, b = range[0], range[1]
                        self.items_placed_i, self.mid = self.tree3.query(a, b)
                        item = self.output_item()
                        self.fitness = 1
                        return item

    # 找fitness==0的矩形
    def find_fitness0_item(self):
        list_r2_w = self.binary_search_range(self.r2, self.s_gap.w, self.r2_i_dict, 1)

        if list_r2_w >= 0:
            self.items_placed_i, self.mid = self.tree2.query(0, list_r2_w)
            # if self.items_placed_i:
            # self.items_placed_i = self.tree2.query(0, list_r2_w)
            item = self.output_item()
            self.fitness = 0
            return item
        else:
            return None

    # 找最合适的矩形
    def find_best_fit_item(self):

        self.prior_next_gap()

        for fitness in (3, 2, 1, 0):
            method = getattr(self, "find_fitness{}_item".format(fitness))
            item = method()
            if item is not None:
                self.fitness = fitness
                return item

        # item = self.find_fitness3_item()
        # if item is not None:
        #     self.fitness = 3
        #     return item
        #
        # item = self.find_fitness2_item()
        # if item is not None:
        #     self.fitness = 2
        #     return item
        #
        # item = self.find_fitness1_item()
        # if item is not None:
        #     self.fitness = 1
        #     return item
        #
        # item = self.find_fitness0_item()
        # if item is not None:
        #     self.fitness = 0
        #     return item

        # if guess_key in self.r1:
        #     self.items_placed_i = self.r1[guess_key][0]
        #     item = self.output_item()
        #     self.fitness = 3
        #     return item
        # elif (self.find_fitness1_item()) is None:
        #     self.find_fitness0_item()

        # elif (self.find_fitness2_item()) is None:
        #     self.find_fitness1_item()
        #     if (self.find_fitness1_item()) is None:
        #         self.find_fitness0_item()
        #         if (self.find_fitness0_item()) is None:
        #             return None

    def raise_gap(self):
        # if min(self.prior_s_gap.y, self.next_s_gap.y) != math.inf:
        #     dummy_item = [self.s_gap.w, min(self.prior_s_gap.y, self.next_s_gap.y)]
        # else:
        dummy_item = [self.s_gap.w, min(self.prior_s_gap.y, self.next_s_gap.y)]
        if self.next_s_gap.y == self.prior_s_gap.y:
            self.fitness = 3
        else:
            self.fitness = 2
        self.update_gaps(dummy_item)


    def pack_item(self, item):
        x, y = 0, 0
        w, h = item[0], item[1]
        if self.fitness == 3 or self.fitness == 2:
            x, y = self.s_gap.x, self.s_gap.y
        if self.fitness == 1:
            if w == self.s_gap.w or h == self.prior_s_gap.y:
                x, y = self.s_gap.x, self.s_gap.y
            elif h == self.next_s_gap.y:
                x, y = self.next_s_gap.x - w, self.s_gap.y
        if self.fitness == 0:
            if self.next_s_gap.y <= self.prior_s_gap.y:
                x, y = self.s_gap.x, self.s_gap.y
            else:
                x, y = self.next_s_gap.x - w, self.s_gap.y

        self.items_placed[-1].append(x)
        self.items_placed[-1].append(y)

    def update_r1(self, guess_key, other_guess_key):
        self.r1[guess_key].remove(self.items_placed_i)
        if len(self.r1[guess_key]) <= 0:
            del self.r1[guess_key]
        if (self.items_placed_i % 2) == 0:
            self.r1[other_guess_key].remove(self.items_placed_i + 1)
            if len(self.r1[other_guess_key]) <= 0:
                del self.r1[other_guess_key]
        else:
            self.r1[other_guess_key].remove(self.items_placed_i - 1)  # 删除r1中已经摆放的和转换长宽的矩形
            if len(self.r1[other_guess_key]) <= 0:
                del self.r1[other_guess_key]

    def update_r2(self, w, h):
        self.r2.remove([w, self.items_placed_i, h])
        if (self.items_placed_i % 2) == 0:
            self.r2.remove([h, self.items_placed_i + 1, w])
        else:
            self.r2.remove([h, self.items_placed_i - 1, w])  # 删除r2中已经摆放的和转换长宽的矩形

    def update_r3(self, w, h):
        self.r3.remove([h, w, self.items_placed_i])
        if (self.items_placed_i % 2) == 0:
            self.r3.remove([w, h, self.items_placed_i + 1])
        else:
            self.r3.remove([w, h, self.items_placed_i - 1])  # 删除r3中已经摆放的和转换长宽的矩形

    def find_tree_index(self, r_dict):
        index = r_dict[self.items_placed_i]
        return index

    def find_tree_other_index(self, r_dict):
        if (self.items_placed_i % 2) == 0:
            other_index = r_dict[self.items_placed_i + 1]
        else:
            other_index = r_dict[self.items_placed_i - 1]
        return other_index

    def update_tree(self):

        index2, index3 = self.find_tree_index(self.r2_i_dict), self.find_tree_index(self.r3_i_dict)

        self.tree2.set(index2, math.inf)
        self.tree3.set(index3, math.inf)

        other_index2, other_index3 = self.find_tree_other_index(self.r2_i_dict), \
                                     self.find_tree_other_index(self.r3_i_dict)
        self.tree2.set(other_index2, math.inf)
        self.tree3.set(other_index3, math.inf)

    def update_items(self, item):
        w, h = item[0], item[1]
        guess_key = self.key(w, h)
        other_guess_key = self.key(h, w)

        self.update_r1(guess_key, other_guess_key)
        self.update_r2(w, h)
        self.update_r3(w, h)

        self.update_tree()

    def result_showing(self):
        x_major_locator, y_major_locator = MultipleLocator(1), MultipleLocator(2)  # 设置x轴、y轴的刻度间隔
        ax = plt.gca()  # ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)
        ax.yaxis.set_major_locator(y_major_locator)
        for (w, h, x, y) in self.items_placed:
            plt.plot([x, x + w, x + w, x, x], [y, y, y + h, y + h, y])  # 由五个点的信息描绘出每个矩形
        plt.show()


    def update_gaps(self, item):
        w, h = item[0], item[1]
        if self.fitness == 3:
            new_gap = Gap(self.prior_s_gap.x, self.prior_s_gap.y,
                          self.prior_s_gap.w + self.s_gap.w + self.next_s_gap.w)  # 更新new gap
            heapq.heappush(self.heap, new_gap)  # 双向链中压入新的gap
            self.heap.remove(self.prior_s_gap)
            self.heap.remove(self.next_s_gap)

            self.double_linked.insert(self.prior_s_gap.prior, new_gap)  # 双向链中更新新的gap
            self.double_linked.delete(self.s_gap, self.next_s_gap)

        if self.fitness == 2:
            if h == self.prior_s_gap.y:
                new_gap = Gap(self.prior_s_gap.x, self.prior_s_gap.y, self.prior_s_gap.w + self.s_gap.w)  # 更新new gap
                heapq.heappush(self.heap, new_gap)  # 双向链中压入新的gap
                self.heap.remove(self.prior_s_gap)

                self.double_linked.insert(self.prior_s_gap.prior, new_gap)  # 双向链中更新新的gap
                self.double_linked.delete(self.s_gap, self.prior_s_gap)

            else:
                new_gap = Gap(self.s_gap.x, self.next_s_gap.y, self.next_s_gap.w + self.s_gap.w)

                heapq.heappush(self.heap, new_gap)  # 双向链中压入新的gap
                self.heap.remove(self.next_s_gap)

                self.double_linked.insert(self.prior_s_gap, new_gap)  # 双向链中更新新的gap
                self.double_linked.delete(self.s_gap, self.next_s_gap)

        if self.fitness == 1:
            if w == self.s_gap.w:
                new_gap = Gap(self.s_gap.x, self.s_gap.y + h, self.s_gap.w)  # 更新new gap

                heapq.heappush(self.heap, new_gap)  # 双向链中压入新的gap
                self.double_linked.insert(self.prior_s_gap, new_gap)  # 双向链中更新新的gap
                self.double_linked.delete(self.s_gap)

            elif h == self.prior_s_gap.y:
                new_gap = Gap(self.prior_s_gap.x, self.prior_s_gap.y, self.prior_s_gap.w + w)  # 更新new gapself.
                new_gap_1 = Gap(self.s_gap.x + w, self.s_gap.y, self.s_gap.w - w)

                heapq.heappush(self.heap, new_gap)  # 双向链中压入新的gap
                heapq.heappush(self.heap, new_gap_1)
                self.heap.remove(self.prior_s_gap)

                self.double_linked.insert(self.prior_s_gap.prior, new_gap)  # 双向链中更新新的gap
                self.double_linked.insert(new_gap, new_gap_1)
                self.double_linked.delete(self.s_gap, self.prior_s_gap)

            elif h == self.next_s_gap.y:
                new_gap = Gap(self.next_s_gap.x - w, self.next_s_gap.y, self.next_s_gap.w + w)
                new_gap_1 = Gap(self.s_gap.x, self.s_gap.y, self.s_gap.w - w)

                heapq.heappush(self.heap, new_gap)  # 双向链中压入新的gap
                heapq.heappush(self.heap, new_gap_1)
                self.heap.remove(self.next_s_gap)

                self.double_linked.insert(self.prior_s_gap, new_gap_1)
                self.double_linked.insert(new_gap_1, new_gap)  # 双向链中更新新的gap
                self.double_linked.delete(self.s_gap, self.next_s_gap)

        if self.fitness == 0:
            if self.prior_s_gap.y >= self.next_s_gap.y:
                new_gap = Gap(self.s_gap.x, h + self.s_gap.y, w)
                new_gap_1 = Gap(self.s_gap.x + w, self.s_gap.y, self.s_gap.w - w)

                heapq.heappush(self.heap, new_gap)  # 双向链中压入新的gap
                heapq.heappush(self.heap, new_gap_1)

                self.double_linked.insert(self.prior_s_gap, new_gap)  # 双向链中更新新的gap
                self.double_linked.insert(new_gap, new_gap_1)
                self.double_linked.delete(self.s_gap)
            else:
                new_gap = Gap(self.next_s_gap.x - w, h + self.s_gap.y, w)
                new_gap_1 = Gap(self.s_gap.x, self.s_gap.y, self.s_gap.w - w)

                heapq.heappush(self.heap, new_gap)  # 双向链中压入新的gap
                heapq.heappush(self.heap, new_gap_1)

                self.double_linked.insert(self.prior_s_gap, new_gap_1)
                self.double_linked.insert(new_gap_1, new_gap)  # 双向链中更新新的gap
                self.double_linked.delete(self.s_gap)

    def packing(self):

        """
        Initialize the skyline
            while not all the rectangles are placed:
                Let s be the bottem-left segment in the skylines
                select r from R
                if r is not found:
                    remove s from the skyline and update
                else :
                    remove r from R and update
            return the height
        """

        self.init()  # 初始化

        while self.not_packed():
            self.s_gap = self.find_lowest_gap()  # 找最合适的gap

            item = self.find_best_fit_item()  # 找最合适的矩形
            print(f"{item=}")
            if item is None:  # 表示没有找到可以放置的矩形
                self.raise_gap()
            else:
                self.pack_item(item)

                self.update_items(item)

                self.update_gaps(item)
        print(self.items_placed)

        self.result_showing()