
# 箱子
class Bin:
    def __init__(self, width, height):
        self.width = width
        self.height = height


# 矩形件
class Item:
    def __init__(self, width, height):
        self.right_top_x = 0
        self.right_top_y = 0
        self.width = width
        self.height = height


# 装箱策略
class Packing:
    def __init__(self):
        pass

    # 将矩形放在右上角，判断是否与箱子中的矩形相交
    @staticmethod
    def overlap(bin_items, new_item, bin_):
        """
        :param bin_: 箱子的尺寸
        :param bin_items: 箱子中所有的items，以列表的形式存储，每个item都是Item的对象
        :param new_item:  需要新放在箱子中的item，也是Item的对象
        :return: flag: if flag = 1 重叠 else 不重叠
        """
        flag = 0  # 初始化
        new_item.right_top_x, new_item.right_top_y = bin_.width, bin_.height
        # 左下角坐标
        left_down_x, left_down_y = new_item.right_top_x - new_item.width, new_item.right_top_y - new_item.height
        if len(bin_items) > 0:  # 如果箱子里面有东西，遍历，看是否重叠。否则肯定不重叠。
            for item in bin_items:
                if item.right_top_x > left_down_x and item.right_top_y > left_down_y:  # 重叠flag=1，一直遍历所有的箱子中的items
                    flag = 1
                    break
                else:
                    flag = 0
        else:
            flag = 0
        return flag

    # 判断两个水平线段是否会相交，同时返回两个水平线段的垂直距离
    @staticmethod
    def horizontal_lines_intersect(line1, line2):
        """
        思路：分5种情况：1）左方不相交；2）左方相交；3）右方相交；4）右方不相交；5）line1完全包含line2
        :param line1: 第一条线段[x1,y1,x2,y2]
        :param line2: 第二条线段[x1,y1,x2,y2]
        :return: flag: if flag = 1 相交 else 相交
                dis:  两条水平线段距离是多少，如果平移动后相交，dis为正数，反之为负数
        """
        # （1）line1完全在line2左方，即line1右端顶点x坐标小于等于line2左端顶点x坐标，且两条线段经过竖直移动后不会相交
        if line1[2] <= line2[0]:
            flag = 0
            dis = line1[1] - line2[1]
        # （2）line1在line2左方，即line1右端顶点x坐标大于line2左端顶点x坐标且小于等于且line2右端顶点x坐标，但两条线段经过竖直移动后会相交
        elif (line1[2] > line2[0]) and (line1[2] <= line2[0]):
            flag = 1
            dis = line1[1] - line2[1]
        # （3）line1在line2右方，即line1左端顶点x坐标大于等于line2左端顶点x坐标且小于且line2右端顶点x坐标，但两条线段经过竖直移动后会相交
        elif (line1[0] >= line2[0]) and (line1[0] < line2[2]):
            flag = 1
            dis = line1[1] - line2[1]
        # （4）line1完全在line2右方，即line1左端顶点x坐标大于等于line2右端顶点x坐标，且两条线段经过竖直移动后不会相交
        elif line1[0] >= line2[2]:
            flag = 0
            dis = line1[1] - line2[1]
        # （5）line1完全包含line2，即line1左端顶点x坐标小于等于line2左端顶点x坐标，line1右端顶点x坐标大于等于line2右端顶点x坐标，且两条线段经过竖直移动后会相交
        else:
            flag = 1
            dis = line1[1] - line2[1]

        return flag, dis

    # 计算下移距离(在箱子的任意位置）
    def down_distance(self, bin_items, new_item):
        """

        :param bin_items:
        :param new_item:
        :return: dis
        """
        down_dis = []
        left_down_x, left_down_y = new_item.right_top_x - new_item.width, new_item.right_top_y - new_item.height
        right_down_x, right_down_y = new_item.right_top_x, new_item.right_top_y - new_item.height
        line1 = [left_down_x, left_down_y, right_down_x, right_down_y]  # new_item的下端线

        if len(bin_items) > 0:
            for item in bin_items:
                line2 = [item.right_top_x - item.width, item.right_top_y, item.right_top_x, item.right_top_y]
                flag, dis_ = self.horizontal_lines_intersect(line1, line2)
                if (flag == 1) and (dis_ >= 0):
                    down_dis.append(dis_)
            if len(down_dis) == 0:  # 没有相交的线段，直接下沉到最底部
                dis = new_item.right_top_y - new_item.height
            else:  # 否则为最小值
                dis = min(down_dis)
        else:
            dis = new_item.right_top_y - new_item.height
        return dis

    # 判断两条竖线是否相交,同时返回两个竖直线段的距离
    @staticmethod
    def vertical_lines_intersect(line1, line2):
        """
        思路：分5种情况：1）上方不相交；2）上方相交；3）下方相交；4）下方不相交；5）line1完全包含line2

        :param line1: 第一条线段[x1,y1,x2,y2]
        :param line2: 第二条线段[x1,y1,x2,y2]
        :return: flag: if flag = 1 相交 else 相交
                dis:  两条竖直线段距离是多少，如果平移动后相交，dis为正数，反之为负数
        """
        # 第一种情况，line1完全在line2上方，且两条线段经过平移后不会相交
        if line1[3] >= line2[1]:
            flag = 0
            dis = line1[0] - line2[0]
        # 第二种情况，line1在line2上方，但两条线段经过平移后会相交
        elif (line1[3] < line2[1]) and (line1[3] >= line2[3]):
            flag = 1
            dis = line1[0] - line2[0]
        # 第三种情况，line1在line2下方，但两条线段经过平移后会相交
        elif (line1[1] <= line2[1]) and (line1[1] > line2[3]):
            flag = 1
            dis = line1[0] - line2[0]
        # 第四种情况，line1完全在line2下方，且两条线段经过平移后不会相交
        elif line1[1] <= line2[3]:
            flag = 0
            dis = line1[0] - line2[0]
        else:
            flag = 1
            dis = line1[0] - line2[0]
        return flag, dis

    # 计算左移距离
    def left_distance(self, bin_items, new_item):
        """

        :param bin_items:
        :param new_item:
        :return: dis
        """

        left_dis = []
        left_up_x, left_up_y = new_item.right_top_x - new_item.width, new_item.right_top_y
        left_down_x, left_down_y = new_item.right_top_x - new_item.width, new_item.right_top_y - new_item.height
        line1 = [left_up_x, left_up_y, left_down_x, left_down_y]  # new_item的左端线

        if len(bin_items) > 0:
            for item in bin_items:
                line2 = [item.right_top_x, item.right_top_y, item.right_top_x, item.right_top_y - new_item.height]
                flag, dis_ = self.vertical_lines_intersect(line1, line2)
                if (flag == 1) and (dis_ >= 0):
                    left_dis.append(dis_)
            if len(left_dis) == 0:  # 没有相交的线段，左移到最左边
                dis = new_item.right_top_x - new_item.width
            else:  # 否则为最小值
                dis = min(left_dis)
        else:
            dis = new_item.right_top_x - new_item.width
        return dis

    # 更新矩形位置
    @staticmethod
    def update_location(new_item, left_dis, down_dis):
        new_item.right_top_x -= left_dis
        new_item.right_top_y -= down_dis


# 初始化
def initialize(items, item_num, my_bin):
    items_ = [Item(items[i][0], items[i][1]) for i in range(item_num)]  # 将物品对象化
    sequence = list(range(item_num))  # 物品排放的顺序
    to_be_scheduled = sequence.copy()  # 复制的待排item，其顺序应该和sequence中的保持一致

    bin_ = Bin(my_bin[0], my_bin[1])
    return items_, sequence, to_be_scheduled, bin_


# 更新已排与未排
def update_list(in_, to_be, item_index, static_items_):
    """

    :param in_: 在箱子中的物品集
    :param to_be: 待排集
    :param item_index: 物品的索引
    :param static_items_: 初始的物品集（对象的实例化）
    :return:
    """
    in_.append(static_items_[item_index])
    to_be.remove(item_index)
