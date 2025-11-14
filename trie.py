"""
Trie数据结构的实现，支持单词存储和查询
"""

from datetime import datetime

class TrieNode:
    """Trie树的节点类"""
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.definition = ""  # 存储单词释义
        self.timestamp = None  # 记录加入时间


class Trie:
    """Trie树的实现，支持高效的前缀查询"""
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str, definition: str = "", timestamp: str = None):
        """
        插入单词及其释义
        
        Args:
            word: 要插入的单词
            definition: 单词的释义
            timestamp: 加入时间（ISO格式），如果为None则使用当前时间
        """
        node = self.root
        word = word.lower().strip()
        
        if not word:
            return False
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        # 如果单词已存在，更新释义
        node.is_end = True
        node.definition = definition
        # 只在新单词时设置时间戳，已存在的单词不更新时间
        if node.timestamp is None:
            node.timestamp = timestamp or datetime.now().isoformat()
        return True
    
    def search(self, word: str) -> tuple:
        """
        查询单词是否存在
        
        Args:
            word: 要查询的单词
            
        Returns:
            (是否存在, 释义, 时间戳)
        """
        node = self.root
        word = word.lower().strip()
        
        for char in word:
            if char not in node.children:
                return False, "", None
            node = node.children[char]
        
        if node.is_end:
            return True, node.definition, node.timestamp
        return False, "", None
    
    def prefix_search(self, prefix: str) -> list:
        """
        前缀查询，返回所有以该前缀开头的单词
        
        Args:
            prefix: 前缀字符串
            
        Returns:
            [(单词, 释义), ...] 列表
        """
        node = self.root
        prefix = prefix.lower().strip()
        
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        result = []
        self._dfs(node, prefix, result)
        return sorted(result, key=lambda x: x[0])
    
    def get_all_words(self) -> list:
        """
        获取所有单词
        
        Returns:
            [(单词, 释义, 时间戳), ...] 列表，按字典序排序
        """
        result = []
        self._dfs(self.root, "", result)
        return sorted(result, key=lambda x: x[0])
    
    def _dfs(self, node: TrieNode, prefix: str, result: list):
        """
        深度优先搜索获取所有单词
        
        Args:
            node: 当前节点
            prefix: 当前前缀
            result: 结果列表
        """
        if node.is_end:
            result.append((prefix, node.definition, node.timestamp))
        
        for char, child_node in node.children.items():
            self._dfs(child_node, prefix + char, result)
    
    def delete(self, word: str) -> bool:
        """
        删除单词
        
        Args:
            word: 要删除的单词
            
        Returns:
            删除是否成功
        """
        def _delete_helper(node: TrieNode, word: str, index: int) -> bool:
            if index == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                node.definition = ""
                return len(node.children) == 0
            
            char = word[index]
            if char not in node.children:
                return False
            
            should_delete_child = _delete_helper(
                node.children[char], word, index + 1
            )
            
            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end
            
            return False
        
        word = word.lower().strip()
        return _delete_helper(self.root, word, 0)
    
    def count(self) -> int:
        """获取单词总数"""
        return len(self.get_all_words())
