from gap import Gap


class DoubleLinkedList:
    def __init__(self, w):
        self.head = Gap(0, float("inf"), 0)
        self.tail = Gap(w, float("inf"), 0)
        self.head.next = self.tail
        self.tail.prior = self.head

    """获取链的长度"""

    def __len__(self):
        length = 0
        node = self.head
        while node != self.tail:
            length += 1
            node = node.next
        return length

    """追加节点"""

    def append(self, node):
        node.next = self.tail
        node.prior = self.tail.prior
        self.tail.prior.next = node
        self.tail.prior = node

        return node

    """插入节点"""

    @staticmethod
    def insert(node_pre, new_node):
        new_node.prior = node_pre
        new_node.next = node_pre.next
        node_pre.next.prior = new_node
        node_pre.next = new_node

    """删除节点"""

    @staticmethod
    def delete(*nodes):
        for node in nodes:
            node.prior.next = node.next
            node.next.prior = node.prior
