"""
词缀管理模块 - 处理词缀归类、查询、释义等功能
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class AffixManager:
    """词缀管理器"""
    
    def __init__(self, storage_path: str = "affixes.json"):
        """初始化词缀管理器"""
        self.storage_path = storage_path
        self.affixes = {}  # {词缀: {定义, 分类, 相关词语}}
        self.load_affixes()
    
    def load_affixes(self):
        """从文件加载词缀"""
        if Path(self.storage_path).exists():
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.affixes = json.load(f)
            except Exception as e:
                print(f"加载词缀失败: {e}")
                self.affixes = {}
        else:
            self.affixes = {}
    
    def save_affixes(self):
        """保存词缀到文件"""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.affixes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存词缀失败: {e}")
    
    def add_affix(self, affix: str, definition: str, category: str = "词缀") -> Tuple[bool, str]:
        """
        添加或更新词缀
        
        Args:
            affix: 词缀（如 "un-", "-tion", "-ly"）
            definition: 词缀释义
            category: 分类（前缀、后缀、中缀等）
        
        Returns:
            (成功与否, 消息)
        """
        affix = affix.strip()
        if not affix:
            return False, "词缀不能为空"
        
        self.affixes[affix] = {
            "definition": definition,
            "category": category,
            "related_words": self.affixes.get(affix, {}).get("related_words", [])
        }
        self.save_affixes()
        return True, f"词缀 '{affix}' 添加/更新成功"
    
    def get_affix_definition(self, affix: str) -> Tuple[bool, str]:
        """获取词缀释义"""
        affix = affix.strip()
        if affix not in self.affixes:
            return False, f"词缀 '{affix}' 不存在"
        
        info = self.affixes[affix]
        return True, f"词缀: {affix}\n类型: {info.get('category', '未分类')}\n释义: {info.get('definition', '无释义')}"
    
    def list_all_affixes(self) -> Tuple[bool, str]:
        """列出所有词缀"""
        if not self.affixes:
            return True, "暂无词缀记录"
        
        # 按分类组织
        by_category = defaultdict(list)
        for affix, info in self.affixes.items():
            category = info.get('category', '未分类')
            by_category[category].append((affix, info.get('definition', '')))
        
        result = f"共有 {len(self.affixes)} 个词缀:\n\n"
        for category in sorted(by_category.keys()):
            result += f"【{category}】\n"
            for affix, definition in sorted(by_category[category]):
                result += f"  • {affix}: {definition}\n"
            result += "\n"
        
        return True, result
    
    def categorize_words(self, words: List[Tuple[str, str]]) -> Dict[str, List[Tuple[str, str]]]:
        """
        根据词缀对单词进行分类
        
        Args:
            words: [(单词, 释义), ...] 列表
        
        Returns:
            {词缀: [(单词, 释义), ...]} 字典
        """
        result = defaultdict(list)
        no_affix = []
        
        for word, definition in words:
            found_affix = False
            # 检查所有已知词缀
            for affix in self.affixes.keys():
                # 检查前缀
                if affix.endswith('-') and word.startswith(affix[:-1]):
                    result[affix].append((word, definition))
                    found_affix = True
                    break
                # 检查后缀
                elif affix.startswith('-') and word.endswith(affix[1:]):
                    result[affix].append((word, definition))
                    found_affix = True
                    break
            
            if not found_affix:
                no_affix.append((word, definition))
        
        if no_affix:
            result['[无匹配词缀]'] = no_affix
        
        return dict(result)
    
    def extract_potential_affixes(self, words: List[str]) -> Dict[str, int]:
        """
        从单词列表中提取潜在的词缀
        
        Args:
            words: 单词列表
        
        Returns:
            {词缀: 出现次数} 字典
        """
        potential_affixes = defaultdict(int)
        min_word_len = 4  # 最小单词长度
        
        # 提取前缀和后缀
        for word in words:
            if len(word) >= min_word_len:
                # 提取可能的前缀（1-3字符）
                for i in range(1, min(4, len(word))):
                    prefix = word[:i]
                    if self._is_valid_affix(prefix):
                        potential_affixes[f"{prefix}-"] += 1
                
                # 提取可能的后缀（1-3字符）
                for i in range(1, min(4, len(word))):
                    suffix = word[-i:]
                    if self._is_valid_affix(suffix):
                        potential_affixes[f"-{suffix}"] += 1
        
        # 过滤出现次数 >= 2 的词缀
        return {k: v for k, v in potential_affixes.items() if v >= 2}
    
    @staticmethod
    def _is_valid_affix(text: str) -> bool:
        """判断是否为有效的词缀候选"""
        return all(c.isalpha() for c in text)
    
    def extract_difference_parts(self, word: str, target_word: str = None) -> List[str]:
        """
        提取单词与已有单词的差异部分（用于fail跳转）
        
        Args:
            word: 查询的单词
            target_word: 如果为None，则返回单词本身；否则提取差异
        
        Returns:
            差异部分列表
        """
        if target_word is None:
            # 返回单词的可能词缀候选
            parts = []
            # 提取前缀
            for i in range(1, min(4, len(word))):
                parts.append(word[:i])
            # 提取后缀
            for i in range(1, min(4, len(word))):
                parts.append(word[-i:])
            return list(set(parts))
        
        # 计算最长公共子序列的差异部分
        min_len = min(len(word), len(target_word))
        common = 0
        for i in range(min_len):
            if word[i] == target_word[i]:
                common += 1
            else:
                break
        
        # 返回差异部分
        diff_parts = []
        if word[:common] != target_word[:common]:
            diff_parts.append(word[:common+1])
        if word[common:]:
            diff_parts.append(word[common:])
        
        return diff_parts if diff_parts else [word]
