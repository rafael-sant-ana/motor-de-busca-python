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
                
class QueryParser:
    def __init__(self):
        self.tokes = []
        self.current_token = 0
    
    def tokenize(self, query):
        tokens = []
        i = 0
        n = len(query)
        
        while i < n:
            char = query[i]
            
            if char.isspace():
                i += 1
                continue
            
            if char in '()':
                tokens.append(char)
                i += 1
                continue
            
            if char.isalpha():
                start = i
                
                while i < n and (query[i].isalpha() or query[i] == '_'):
                    i += 1
                
                word = query[start:i].upper()
                
                if word in ['AND', 'OR']:
                    tokens.append(word)
                else:
                    tokens.append(word)
                continue
            
            i += 1
            
        return tokens

    def parse(self, query):
        self.tokens = self.tokenize(query)
        self.current_token = 0
        return self. parse_expression()
    
    def get_current_token(self):
        if self.current_token < len(self.tokens):
            return self.tokens[self.current_token]
        return None
    
    def consume(self, expected=None):
        if self.current_token >= len(self.tokens):
            if expected:
                raise SyntaxError(f"Esperado '{expected}', mas não há mais toquens'")
            return None
        
        token = self.tokens[self.current_token]
        
        if expected and token != expected:
            raise SyntaxError(f"Esperado '{expected}', mas encontrado '{token}'")
        
        self.current_token += 1
        return token
    
    def parse_expression(self):
        return self.parse_or_expression()
    
    def parse_or_expression(self):
        left = self.parse_and_expression()
        
        while self.get_current_token() == 'OR':
            operator = self.consume('OR')
            right = self.parse_and_expression()
            left = ASTnode('OPERATOR', operator, left, right)
            
        return left
    
    def parse_and_expression(self):
        left = self.parse_primary()
        
        while self.get_current_token() == 'AND':
            operator = self.consume('AND')
            right = self.parse_primary()
            left = ASTnode('OPERATOR', operator, left, right)
            
        return left
    
    def parse_primary(self):
        token = self.get_current_token()
        
        if token == '(':
            self.consume('(')
            expression = self.parse_expression()
            
            if self.get_current_token() != ')':
                raise SyntaxError("Esperado fechamento de parentêses")
            
            self.consume(')')
            return expression
        
        elif token and token not in ('AND', 'OR', ')'):
            term = self.consume()
            return ASTnode('TERM', term)
        else:
            raise SyntaxError(f"Token inesperado: '{token}'")

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
