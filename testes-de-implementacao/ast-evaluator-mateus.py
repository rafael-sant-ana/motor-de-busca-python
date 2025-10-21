class ASTEvaluator:
    def __init__(self, inverted_index):
        self.inverted_index = inverted_index
        
    def evaluate(self, node):
        if node.node_type == 'TERM':
            return self.inverted_index.get(node.value, set())
        
        elif node.node_type == 'OPERATOR':
            left_docs = self.evaluate(node.leftChild)
            right_docs = self.evaluate(node.rightChild)
            
            if node.value == 'AND':
                return left_docs & right_docs
            elif node.value == 'OR':
                return left_docs | right_docs
            
        return set()
