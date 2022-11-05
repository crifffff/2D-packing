from BL_packing import *
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# 输入数据
random.seed(10)


items = [(random.randint(1, 5), random.randint(1, 5)) for i in range(30)]  # item的列表,随机生成30个
static_items_ = [Item(items[i][0], items[i][1]) for i in range(len(items))]  # 将物品实例化
my_bin = (20, 10)  # 箱子的尺寸信息
my_bin_ = Bin(my_bin[0], my_bin[1])  # 箱子实例化

# #   BL（bottom-up left-justified）法求解二位装箱问题
# #   思想：首先将选中的物体放在箱子的右上角，然后尽量向下向左作连续移动，直到不能移动为止
# 简化按照随机生成的箱子的顺序排


def pack(my_items, bin_num):
    bin_num += 1  # 箱子计数
    item_num = len(my_items)
    items_, sequence, to_be_scheduled, bin_ = initialize(my_items, item_num, my_bin)  # 初始化
    bin_items = []
    test_pack = Packing()
    for i in sequence:
        over_flag = test_pack.overlap(bin_items, static_items_[i], bin_)  # 判断是否可以放下
        if over_flag == 1:
            continue
        else:
            while 1:  # 执行下移与左移，直到不能移动
                down_dis = test_pack.down_distance(bin_items, static_items_[i])
                left_dis = 0
                test_pack.update_location(static_items_[i], left_dis, down_dis)

                left_dis = test_pack.left_distance(bin_items, static_items_[i])
                down_dis = 0
                test_pack.update_location(static_items_[i], left_dis, down_dis)

                if down_dis == 0 and left_dis == 0:
                    update_list(bin_items, to_be_scheduled, i, static_items_)
                    break
    # 换箱子
    # if len(to_be_scheduled) > 0:
    #     pack(to_be_scheduled)
    return bin_num, bin_items


bin_num_, bin_items_ = pack(items, 0)
print("There are {} items".format(len(bin_items_)))

# 计算箱子的利用率
rect_area = 0
bin_area = my_bin_.height * my_bin_.width
for item in bin_items_:
    rect_area += item.width * item.height
rate = rect_area / bin_area
print("The packing rate is {}%".format(rate * 100))


# 画图
fig, ax = plt.subplots(1, 1)
ax1 = fig.gca()
for item in bin_items_:
    rx, ry = item.right_top_x, item.right_top_y
    lx, ly = rx - item.width, ry - item.height
    plt.xlim((0, my_bin_.width))
    plt.ylim((0, my_bin_.height))
    color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    rect = patches.Rectangle((lx, ly), item.width, item.height, linewidth=1, facecolor=color)
    ax1.add_patch(rect)
plt.show()
