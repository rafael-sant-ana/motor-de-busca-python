class ASTnode:
    def __init__(self, node_type, value=None, leftChild=None, rightChild=None, parent= None):
        self.node_type = node_type
        self.value = value
        self.leftChild = leftChild
        self.rightChild = rightChild
        self.parent = None
    
    def __str__(self):
        if self.node_type == 'TERM':
            return f'TERM({self.value})'
        else:
            return f'OP({self.value})'

class AST:
    def __init__(self):
        self.root = None
        
    def set_root(self, node):
        self.root = node
        
    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        if node is not None:
            print(" " * level + str(node))
            if node.leftChild:
                self.print_tree(node.leftChild, level + 1)
            if node.rightChild:
                self.print_tree(node.rightChild, level + 1)