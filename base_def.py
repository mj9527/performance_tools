

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.child_list = []


class StackInfo:
    def __init__(self, frame_list, weight):
        self.frame_list = frame_list
        self.weight = weight


class FrameInfo:
    def __init__(self, index, address, func_name, module, weight):
        self.index = index
        self.address = address
        self.func_name = func_name
        self.module = module
        self.self_weight = weight
        self.all_weight = weight
