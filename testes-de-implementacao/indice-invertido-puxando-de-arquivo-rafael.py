import os
import re


class Node:
    def __init__(self, value, position=None):
        self.children = {}
        self.value = value
        self.is_end = True
        self.positions = {}

        if position:
            self.append_occourence(position)

    def append_occourence(
        self, position_metadata
    ):  # position_metadata = { path: '', position: 0 }
        path = position_metadata["path"]
        position = position_metadata["position"]

        if path not in self.positions:
            self.positions[path] = []

        self.positions[path].append(position)

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

    def insert_rec(self, root, value, position, path):
        if len(value) == 0:
            return
        # consome o maximo da palavra
        i = self.consume_word(root.value, value)
        rest_value = value[i:]

        metadata_node_insertion = {"path": path, "position": position}

        # exemplo, estamos inserindo "chae" em "chave"
        if i < len(root.value):
            rest_root = root.value[i:]

            # cria um novo pra ter tudo que a raiz tinha
            child = Node(rest_root)
            child.children = root.children
            child.is_end = root.is_end
            child.positions = root.positions

            root.value = root.value[:i]
            root.is_end = False
            root.children = {child.value[0]: child}
            root.positions = {}

            if rest_value:  # exemplo, inserindo chae em chave, precisamos colocar "e" como sendo fim, e "ve" tambem
                root.add_child(Node(rest_value, metadata_node_insertion))

            else:  # exemplo, inserindo cha em chave
                # nosso root seria cha
                root.is_end = True

        else:  # i >= lenroot val quer dizer, inserindo "chavea" e, "chave"
            if not rest_value:  # inserindo chave em chave
                root.is_end = True
                root.append_occourence(metadata_node_insertion)
            else:  # ainda temos um a pra inserir em algum filho
                next_child = root.retrieve_child(rest_value)
                if next_child:  # inserir "chaveabe" depois de ter "chave" e "chavea"
                    self.insert_rec(next_child, value, position, path)
                else:  # inserir "chavea" e n tem nada com o prefixo "a" depois de "chave"
                    root.add_child(Node(rest_value, metadata_node_insertion))

    def insert(self, value, position, path):
        self.insert_rec(self.head, value, position, path)

    def find(self, word):
        word_tot_length = len(word)
        consumed_so_far = 0
        root = self.head

        while root is not None:
            print("value=", root.value)
            print("word=", word)
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
            print(
                f"{indent}└── '{child.value}'{end_marker} ({','.join(str(x) for x in child.positions)})"
            )
            self.log_tree(child, indent + "    ")

    # quero gerar todas as palavras de volta. pensei numa DFS para ir construindo palavra-a-palavra.
    def construct_index(self):
        root = self.head

        words = []

        def dfs(root, prefix):
            if root is None:
                words.append(prefix)
                return

            prefix_appended = prefix + root.value

            if root.is_end:
                words.append(prefix_appended)

            for _, child in sorted(root.children.items()):
                dfs(child, prefix_appended)

        dfs(root, "")

        return "\n".join(str(x) for x in words)


if __name__ == "__main__":
    folder_path = "bbc/business"
    txt_contents = {}

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith(".txt"):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        txt_contents[file_path] = f.read()
                except Exception as e:
                    print(f"⚠️ Could not read {file_path}: {e}")

    trie = TrieCompacta()

    for path, text in txt_contents.items():
        print(path)
        for idx, word in enumerate(re.split(r"[ \n]+", text)):
            trie.insert(word, idx, path)

    search_term = "sales"

    search_term = search_term.lower()

    print("---")

    print(trie.find(search_term))
