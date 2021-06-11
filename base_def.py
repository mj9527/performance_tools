
class NodeInfo:
    def __init__(self, thread_id, node):
        self.node = node
        self.thread_id = thread_id
        self.child_list = []


class FrameInfo:
    def __init__(self, index, address, weight):
        self.index = index
        self.address = address
        self.self_weight = weight
        self.all_weight = weight
        self.func_name = ""
        self.module = ""