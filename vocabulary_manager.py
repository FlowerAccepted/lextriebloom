"""
单词积累本的存储和管理模块，支持多种格式的持久化
"""

import json
import pickle
from pathlib import Path
from typing import Optional
from abc import ABC, abstractmethod

from trie import Trie


class StorageBackend(ABC):
    """存储后端的抽象基类，便于扩展"""
    
    @abstractmethod
    def save(self, trie: Trie, filepath: str) -> bool:
        """保存Trie到文件"""
        pass
    
    @abstractmethod
    def load(self, filepath: str) -> Optional[Trie]:
        """从文件加载Trie"""
        pass


class PickleStorage(StorageBackend):
    """使用pickle格式存储"""
    
    def save(self, trie: Trie, filepath: str) -> bool:
        """使用pickle保存Trie"""
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(trie, f)
            return True
        except Exception as e:
            print(f"Pickle保存失败: {e}")
            return False
    
    def load(self, filepath: str) -> Optional[Trie]:
        """使用pickle加载Trie"""
        try:
            with open(filepath, 'rb') as f:
                trie = pickle.load(f)
            return trie
        except Exception as e:
            print(f"Pickle加载失败: {e}")
            return None


class JSONStorage(StorageBackend):
    """使用JSON格式存储"""
    
    def save(self, trie: Trie, filepath: str) -> bool:
        """使用JSON保存Trie（转换为字典形式）"""
        try:
            words = trie.get_all_words()
            data = {
                "words": [
                    {"word": word, "definition": definition}
                    for word, definition in words
                ]
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"JSON保存失败: {e}")
            return False
    
    def load(self, filepath: str) -> Optional[Trie]:
        """使用JSON加载Trie"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            trie = Trie()
            for item in data.get("words", []):
                word = item.get("word", "")
                definition = item.get("definition", "")
                if word:
                    trie.insert(word, definition)
            return trie
        except Exception as e:
            print(f"JSON加载失败: {e}")
            return None


class VocabularyManager:
    """单词积累本管理器"""
    
    def __init__(self, storage_backend: StorageBackend = None):
        """
        初始化管理器
        
        Args:
            storage_backend: 存储后端，默认使用JSON格式
        """
        self.trie = Trie()
        self.storage = storage_backend or JSONStorage()
        self.filepath = None
    
    def add_word(self, word: str, definition: str = "") -> tuple:
        """
        添加单条单词
        
        Args:
            word: 单词
            definition: 释义
            
        Returns:
            (成功与否, 消息)
        """
        if not word.strip():
            return False, "单词不能为空"
        
        success = self.trie.insert(word, definition)
        if success:
            return True, f"单词 '{word}' 添加成功"
        return False, f"单词 '{word}' 添加失败"
    
    def import_from_file(self, filepath: str) -> tuple:
        """
        从文件导入单词（格式：每行一个 "单词 释义"）
        
        Args:
            filepath: 文件路径
            
        Returns:
            (成功与否, 消息)
        """
        try:
            count = 0
            errors = []
            
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):  # 支持注释行
                        continue
                    
                    parts = line.split(None, 1)  # 按空格分割，最多分为2部分
                    if len(parts) < 1:
                        continue
                    
                    word = parts[0]
                    definition = parts[1] if len(parts) > 1 else ""
                    
                    if self.trie.insert(word, definition):
                        count += 1
                    else:
                        errors.append(f"行 {line_num}: {word} 导入失败")
            
            msg = f"成功导入 {count} 个单词"
            if errors:
                msg += f"，失败 {len(errors)} 个: " + "; ".join(errors[:3])
            
            return True, msg
        except FileNotFoundError:
            return False, f"文件不存在: {filepath}"
        except Exception as e:
            return False, f"导入文件时出错: {e}"
    
    def search_word(self, word: str) -> tuple:
        """
        查询单词
        
        Args:
            word: 要查询的单词
            
        Returns:
            (是否存在, 释义或错误消息)
        """
        exists, definition = self.trie.search(word)
        if exists:
            return True, f"单词: {word}\n释义: {definition}"
        return False, f"单词 '{word}' 不存在"
    
    def prefix_search(self, prefix: str) -> tuple:
        """
        前缀查询
        
        Args:
            prefix: 前缀
            
        Returns:
            (是否找到, 结果字符串或错误消息)
        """
        if not prefix.strip():
            return False, "前缀不能为空"
        
        results = self.trie.prefix_search(prefix)
        if not results:
            return False, f"没有找到以 '{prefix}' 开头的单词"
        
        result_str = f"找到 {len(results)} 个单词:\n"
        for word, definition in results[:50]:  # 最多显示50个
            result_str += f"• {word}: {definition}\n"
        
        if len(results) > 50:
            result_str += f"\n... 还有 {len(results) - 50} 个单词"
        
        return True, result_str
    
    def list_all_words(self) -> tuple:
        """
        列出所有单词
        
        Returns:
            (是否成功, 结果字符串)
        """
        words = self.trie.get_all_words()
        if not words:
            return True, "单词本为空"
        
        result_str = f"共有 {len(words)} 个单词:\n"
        for word, definition in words[:100]:  # 最多显示100个
            result_str += f"• {word}: {definition}\n"
        
        if len(words) > 100:
            result_str += f"\n... 还有 {len(words) - 100} 个单词"
        
        return True, result_str
    
    def delete_word(self, word: str) -> tuple:
        """
        删除单词
        
        Args:
            word: 要删除的单词
            
        Returns:
            (成功与否, 消息)
        """
        if self.trie.delete(word):
            return True, f"单词 '{word}' 删除成功"
        return False, f"单词 '{word}' 不存在或删除失败"
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "total_words": self.trie.count(),
            "storage_type": self.storage.__class__.__name__
        }
    
    def save(self, filepath: str) -> tuple:
        """
        保存到文件
        
        Args:
            filepath: 保存路径
            
        Returns:
            (成功与否, 消息)
        """
        self.filepath = filepath
        if self.storage.save(self.trie, filepath):
            return True, f"保存成功到 {filepath}"
        return False, f"保存失败"
    
    def load(self, filepath: str) -> tuple:
        """
        从文件加载
        
        Args:
            filepath: 加载路径
            
        Returns:
            (成功与否, 消息)
        """
        loaded_trie = self.storage.load(filepath)
        if loaded_trie:
            self.trie = loaded_trie
            self.filepath = filepath
            count = self.trie.count()
            return True, f"加载成功，共 {count} 个单词"
        return False, "加载失败"
    
    def export_to_file(self, filepath: str, format: str = "txt") -> tuple:
        """
        导出单词到文件
        
        Args:
            filepath: 导出路径
            format: 导出格式 (txt, json, csv)
            
        Returns:
            (成功与否, 消息)
        """
        try:
            words = self.trie.get_all_words()
            
            if format == "txt":
                with open(filepath, 'w', encoding='utf-8') as f:
                    for word, definition in words:
                        f.write(f"{word} {definition}\n")
            elif format == "json":
                data = {
                    "words": [
                        {"word": word, "definition": definition}
                        for word, definition in words
                    ]
                }
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            elif format == "csv":
                with open(filepath, 'w', encoding='utf-8', newline='') as f:
                    f.write("word,definition\n")
                    for word, definition in words:
                        # 简单的CSV转义
                        escaped_def = definition.replace('"', '""')
                        f.write(f'"{word}","{escaped_def}"\n')
            else:
                return False, f"不支持的格式: {format}"
            
            return True, f"导出成功到 {filepath}"
        except Exception as e:
            return False, f"导出失败: {e}"
