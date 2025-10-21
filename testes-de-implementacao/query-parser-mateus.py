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
    
    def parse_primery(self):
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
