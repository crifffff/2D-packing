import random
from random_ls import *
import numpy as np
from pymoo.core.problem import Problem
from typing import Iterable, Dict


class ISB(Problem):
    def __init__(self,
                 items: Dict[int, list] = None,
                 width: int = None,
                 **kwargs: Dict):
        self.items = items
        self.width = width
        super(ISB, self).__init__(
            n_var=len(items),
            n_obj=1,
            elementwise=True,  # 逐个解码，即传入_evaluate的x为单个个体的染色体编码
            **kwargs
        )

    def _evaluate(self, x, out, *args, **kwargs):
        """

        :param x: 单个个体的染色体，items的序列，np.array([int])
        :param out: 评价结果，dict
        :param args: 其他参数
        :param kwargs: 其他参数
        :return:
        """
        items_list = []
        for i in x:
            items_list.append(self.items[i])
        improved = ImprovedSkylineBased(items_list, self.width)
        best_h = improved.packing()
        items_placed = improved.result()
        out["X"] = x
        out["F"] = np.array(best_h)
        out["items_placed"] = np.array([items_placed])


# random
def main():
    # 给定相关值或者读取相关值
    from data import get_default_data
    w = 100
    # all_items = [[30, 20], [15, 27], [13, 21], [50, 26], [39, 49], [15, 38], [13, 15],
    #              [29, 67], [9, 17], [20, 57], [39, 27]]

    all_items = get_default_data(60, (10, 40), (15, 60))
    items_list = []
    for i in all_items:
        items_list.append(all_items[i])

    rules = ["sort by height in decreasing", "sort by width in decreasing"]
    best_items = random_ls(items_list, w, rules)
    improved = ImprovedSkylineBased(best_items, w)
    # improved = ImprovedSkylineBased(all_items, w)

    best_item_ = improved.packing()
    best_h = best_item_[3] + best_item_[1]
    items_placed = improved.result()
    print(best_h, items_placed)


if __name__ == '__main__':
    from data import get_default_data
    from pymoo.algorithms.soo.nonconvex.ga import GA
    from sampling import ISBSampling
    from pymoo.operators.crossover.ox import OrderCrossover
    from pymoo.operators.mutation.inversion import InversionMutation
    from pymoo.termination.max_gen import MaximumGenerationTermination

    def test(
            n_items: int = 10,
            item_w_range: tuple = (10, 50),
            item_h_range: tuple = (50, 70),
            width: int = 100,
            seed=None,
            pop_size=100,
            crossover_prob=0.8,
            mutation_prob=0.1,
            n_max_gen=150,
            sampling_=ISBSampling()
    ):
        # 生成数据
        items_ = get_default_data(n_items, item_w_range, item_h_range)
        # 实例化问题
        problem = ISB(items_, width)
        # 实例化算法
        algorithm = GA(
            pop_size=pop_size,
            sampling=sampling_,
            crossover=OrderCrossover(prob=crossover_prob),
            mutation=InversionMutation(prob=mutation_prob)
        )
        # 算法设置
        algorithm.setup(
            problem=problem,
            termination=MaximumGenerationTermination(n_max_gen=n_max_gen),
            verbose=True
        )
        # 算法运行
        res = algorithm.run()
        # 获取最佳个体
        best_individual = res.opt[0]
        # 输出适应度值
        print(best_individual.get('F'))
        # 输出计划方案
        print(best_individual.get('items_placed'))
        print(best_individual.get('X'))

        # # 绘制迭代图
        # draw(algorithm.callback.data)

    test()
