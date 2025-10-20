class ASTnode:
    def __init__(self, node_type, value=None, leftChildren=None, rightChildren=None, parent= None):
        self.node_type = node_type
        self.value = value
        self.leftChildren = leftChildren
        self.rightChildren = rightChildren
        self.parent = None

class AST:
    def __init__(self):
        self.root = None
        
    def set_root(self, node):
        self.root = node