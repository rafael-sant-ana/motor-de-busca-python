class Node:
    def __init__(self, value):
        self.children = {}
        self.value = value

    def add_child(self, node):
        if len(node.value) == 0:
            return
        self.children[node.value[0]] = node

    def retrieve_child(self, val):
        if isinstance(val, Node):
            node = val
            if len(node.value) == 0:
                return None
        
            return self.children.get(node.value[0], None)

        if isinstance(val, str):
            if len(val) == 0:
                return None
            
            return self.children.get(val[0], None)

class TrieCompacta:
    def __init__(self):
        self.head = Node("")
    
    def consume_word(self, value1, value2):
        i = 0
        j = min(len(value1), len(value2))
        while i < j and value1[i] == value2[i]:
            i = i+1

        return i

    def insert_rec(self, root, node_value):
        # consome o maximo da palavra
        i = self.consume_word(root.value, node_value.value)        

        # atualiza pra de fato consumir a palavra        
        node_value.value = node_value.value[i:]

        # o no de agora tem que ir ate onde da pra consumir, e temos uma nova variavel rest_of_curr pro que sobrou
        rest_of_curr = root.value[i:]
        root.value = root.value[:i]

        # coloca oq sobrou num no
        node_rest_of_curr = Node(rest_of_curr)

        # ve pra onde essses 2 nos devia ir        
        node_rest_of_curr_should_go_to = root.retrieve_child(node_rest_of_curr)
        node_node_value_should_go_to = root.retrieve_child(node_value)

        # e insere conforme adequado
        for target, node in (
            (node_node_value_should_go_to, node_value),
            (node_rest_of_curr_should_go_to, node_rest_of_curr),
        ):
            if target is None:
                root.add_child(node)
            else:
                self.insert_rec(target, node)


    def insert(self, value):
        node_value = Node(value)
        self.insert_rec(self.head, node_value)

    def find(self, word):
        word_tot_length = len(word)
        consumed_so_far = 0
        root = self.head

        while root != None:
            i = self.consume_word(root.value, word)
            consumed_so_far = consumed_so_far + i

            word = word[i:]
            next_dir = root.retrieve_child(word)
            rest_len = len(root.value[i:])

            if consumed_so_far == word_tot_length and rest_len == 0:
                return root

            if not next_dir:
                return None

            root = next_dir
        
        return None

    def log_tree(self):
        self.log_tree_rec(self.head)

    def log_tree_rec(self, root):
        print(root.value)

        for _, val in root.children.items():
            self.log_tree_rec(val)



if __name__ == "__main__":
    trie = TrieCompacta()

    trie.insert("car")
    trie.insert("cart")

    print(trie.find("cart"))

    #trie.log_tree()
