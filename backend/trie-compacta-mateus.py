class Node:
    def __init__(self, value=""):
        self.children = {}
        self.value = value
        self.is_the_end = False

class TrieCompacta:
    def __init__(self):
        self.root = Node("")
        
    def find(self, word):
        current = self.root
        i = 0
        
        while i < len(word):
            if word[i] in current.children:
                child = current.children[word[i]]
                label = child.value
                j = 0
                
                while j < len(label) and i < len(word) and label[j] == word[i]:
                    j += 1
                    i += 1
                
                if j < len(label):
                    return False
                current = child
            
            else:
                return False
        return current.is_the_end
    
    def insert(self, word):
        current = self.root
        i = 0
        while i < len(word):
            if word[i] in current.children:
                child = current.children[word[i]]
                label = child.value
                j = 0
                
                while j < len(label) and i < len(word) and label[j] == word[i]:
                    j += 1
                    i += 1
                    
                if j == len(label):
                    current = child
                    
                    if i == len(word):
                        child.is_the_end = True
                        return
                else:
                    existing_child = Node(label[j:])
                    existing_child.children = child.children
                    existing_child.is_the_end = child.is_the_end
                    
                    child.value = label[:j]
                    child.children = {existing_child.value[0]: existing_child}
                    child.is_the_end = False
                    
                    if i < len(word):
                        new_child = Node(word[i:])
                        new_child.is_the_end = True
                        child.children[word[i]] = new_child
                        return
                    else:
                        child.is_the_end = True
                        return
            else:
                new_child = Node(word[i:])
                new_child.is_the_end = True
                current.children[new_child.value[0]] = new_child
                return
    
    def print_trie(self):
        def _print(node, prefix):
            if node.is_the_end:
                print(prefix)
            for child in node.children.values():
                _print(child, prefix + " " + child.value + "\n")
                
        _print(self.root, "")
        
if __name__ == "__main__":
    trie = TrieCompacta()
    trie.insert("team")
    trie.insert("test")
    
    trie.insert("chave")
    trie.insert("cha")
    
    trie.print_trie()
    print()
    print()