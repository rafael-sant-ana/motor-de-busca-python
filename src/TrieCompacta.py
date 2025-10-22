import json
from glob import glob
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
    ): 
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
        
    def to_dict(self):
        return {
            'value': self.value,
            'is_end': self.is_end,
            'positions': self.positions,
            'children': {k: v.to_dict() for k, v in self.children.items()}
        }

class TrieCompacta:
    def __init__(self):
        self.head = Node("")
        self.head.is_end = True
        self.num_docs = 0

    def consume_word(self, value1, value2):
        i = 0
        j = min(len(value1), len(value2))
        while i < j and value1[i] == value2[i]:
            i = i + 1
        return i

    def insert_rec(self, root, value, position, path):
        if len(value) == 0:
            return
        
        i = self.consume_word(root.value, value)
        rest_value = value[i:]
        metadata_node_insertion = {"path": path, "position": position}

        if i < len(root.value):
            rest_root = root.value[i:]

            child = Node(rest_root)
            child.children = root.children
            child.is_end = root.is_end
            child.positions = root.positions

            root.value = root.value[:i]
            root.is_end = False
            root.children = {child.value[0]: child}
            root.positions = {}

            if rest_value:
                root.add_child(Node(rest_value, metadata_node_insertion))
            else:
                root.is_end = True
                root.append_occourence(metadata_node_insertion)

        else:
            if not rest_value:
                root.is_end = True
                root.append_occourence(metadata_node_insertion)
            else:
                next_child = root.retrieve_child(rest_value)
                if next_child:
                    self.insert_rec(next_child, rest_value, position, path)
                else:
                    root.add_child(Node(rest_value, metadata_node_insertion))

    def insert(self, value, position, path):
        self.insert_rec(self.head, value, position, path)

    def find(self, word):
        word_tot_length = len(word)
        consumed_so_far = 0
        root = self.head

        while root is not None:
            i = self.consume_word(root.value, word)
            consumed_so_far = consumed_so_far + i

            word = word[i:]
            next_dir = root.retrieve_child(word)
            rest_len = len(root.value[i:])

            if consumed_so_far == word_tot_length and rest_len == 0:
                return root if root.is_end else None

            if not next_dir:
                return None
            
            if len(word) == 0: 
                return root if root.is_end and rest_len == 0 else None

            root = next_dir

        return None

    def to_dict(self):
        return self.head.to_dict()
    
    def from_dict(self, data):
        def build_node(node_data):
            node = Node(node_data['value'])
            node.is_end = node_data['is_end']
            node.positions = node_data['positions']
            for k, v in node_data['children'].items():
                child_node = build_node(v)
                node.children[k] = child_node
            return node
        
        self.head = build_node(data)


def initialize_index(trie, folder_path="bbc", index_file="trie_index.json"):
  # o has_found simboliza se ja tem o index_file criado
  has_found = False
  
  try:
      with open(index_file, "r", encoding="utf-8") as f:
          data = json.load(f)
          trie.from_dict(data['trie'])
          trie.num_docs = data['num_docs']
          has_found = True
  except:
      pass

  if not has_found:
      txt_contents = {}
      pattern = os.path.join(folder_path, "**", "*.txt")
      num_docs = 0

      for file_path in glob(pattern, recursive=True):
          num_docs += 1
          try:
              with open(file_path, "r", encoding="utf-8") as f:
                  txt_contents[file_path] = f.read().lower()
          except:
            pass  

      trie.num_docs = num_docs
      
      for path, text in txt_contents.items():
          words = [word for word in re.split(r'[^a-z0-9]+', text) if word]
          
          start_pos = 0
          for word in words:
              where_happens = text.find(word, start_pos)
              
              offset = where_happens + 1 
              trie.insert(word, offset, path)
              
              start_pos = where_happens

      try:
          with open(index_file, "w", encoding="utf-8") as f:
              json.dump({'trie': trie.to_dict(), 'num_docs': trie.num_docs}, f, indent=2)
      except:
          pass
