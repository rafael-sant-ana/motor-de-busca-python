class TrieAdapter:
    def __init__(self, trie):
        self.trie = trie
        self._build_path_mapping()
        
    def _build_path_mapping(self):
        self.path_to_id = {}
        self.id_to_path = {}
        all_paths = set()
        
        def collect_paths(node):
            if hasattr(node, 'positions') and node.positions:
                all_paths.update(node.positions.keys())
            if hasattr(node, 'children'):
                for child in node.children.values():
                    collect_paths(child)
        
        collect_paths(self.trie.head)
        
        for idx, path in enumerate(sorted(all_paths)):
            doc_id = idx + 1
            self.path_to_id[path] = doc_id
            self.id_to_path[doc_id] = path
            
    def get(self, term, default=None):
        node = self.trie.find(term)
        
        if node is None or not node.is_end:
            return default if default is not None else []
        
        document_ids = [(self.path_to_id[path], value) for path, value in node.positions.items() if path in self.path_to_id]
        
        return document_ids
    
    def get_document_path(self, doc_id):
        return self.id_to_path.get(doc_id)
    
    def get_all_documents(self):
        return set(self.path_to_id.values())