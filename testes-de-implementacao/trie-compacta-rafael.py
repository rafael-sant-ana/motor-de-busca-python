class Node:
    def __init__(self, value):
        self.children = {}
        self.value = value
        self.is_end = True

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
        self.head.is_end = True

    def consume_word(self, value1, value2):
        i = 0
        j = min(len(value1), len(value2))
        while i < j and value1[i] == value2[i]:
            i = i + 1

        return i

    def insert_rec(self, root, value):
        if len(value) == 0:
            return
        # consome o maximo da palavra
        i = self.consume_word(root.value, value)
        rest_value = value[i:]

        # exemplo, estamos inserindo "chae" em "chave"
        if i < len(root.value):
            rest_root = root.value[i:]

            # cria um novo pra ter tudo que a raiz tinha
            child = Node(rest_root)
            child.children = root.children
            child.is_end = root.is_end

            root.value = root.value[:i]
            root.is_end = False
            root.children = {child.value[0]: child}

            if rest_value:  # exemplo, inserindo chae em chave, precisamos colocar "e" como sendo fim, e "ve" tambem
                root.add_child(Node(rest_value))

            else:  # exemplo, inserindo cha em chave
                # nosso root seria cha
                root.is_end = True

        else:  # i >= lenroot val quer dizer, inserindo "chavea" e, "chave"
            if not rest_value:  # inserindo chave em chave
                root.is_end = True
            else:  # ainda temos um a pra inserir em algum filho
                next_child = root.retrieve_child(rest_value)

                if next_child:  # inserir "chaveabe" depois de ter "chave" e "chavea"
                    self.insert_rec(next_child, value)
                else:  # inserir "chavea" e n tem nada com o prefixo "a" depois de "chave"
                    root.add_child(Node(rest_value))

    def insert(self, value):
        self.insert_rec(self.head, value)

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
                return root if root.is_end else None

            if not next_dir:
                return None

            root = next_dir

        return None

    def log_tree(self, node=None, indent=""):
        if node is None:
            node = self.head
            print("'' (raiz)")

        for _, child in sorted(node.children.items()):
            end_marker = " (End) " if child.is_end else ""
            print(f"{indent}└── '{child.value}'{end_marker}")
            self.log_tree(child, indent + "    ")


if __name__ == "__main__":
    trie = TrieCompacta()

    trie.insert("chave")
    trie.insert("cha")

    print(trie.find("cha"))

    trie.log_tree()
