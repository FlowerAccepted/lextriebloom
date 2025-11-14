"""
统计分析模块 - 处理单词加入时间统计、热力图等
"""

from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


class StatisticsAnalyzer:
    """统计分析器"""
    
    def __init__(self):
        """初始化统计分析器"""
        pass
    
    @staticmethod
    def get_daily_statistics(words_data: List[Tuple[str, str, Optional[str]]]) -> Dict[str, int]:
        """
        按日期统计单词数量
        
        Args:
            words_data: [(单词, 释义, 时间戳), ...] 列表
        
        Returns:
            {日期(YYYY-MM-DD): 单词数} 字典
        """
        daily_count = defaultdict(int)
        
        for word, definition, timestamp in words_data:
            if timestamp:
                try:
                    # 从ISO格式时间戳提取日期
                    dt = datetime.fromisoformat(timestamp)
                    date_str = dt.strftime("%Y-%m-%d")
                    daily_count[date_str] += 1
                except Exception:
                    pass
        
        return dict(sorted(daily_count.items()))
    
    @staticmethod
    def generate_heatmap_text(daily_stats: Dict[str, int]) -> str:
        """
        生成文本格式的热力图
        
        Args:
            daily_stats: {日期: 数量} 字典
        
        Returns:
            热力图文本
        """
        if not daily_stats:
            return "暂无统计数据"
        
        # 按日期排序
        sorted_dates = sorted(daily_stats.items())
        
        # 计算热度等级
        max_count = max(daily_stats.values()) if daily_stats else 1
        
        result = "📊 每日加入统计热力图\n"
        result += "="*60 + "\n"
        
        current_date = None
        week_data = []
        
        for date_str, count in sorted_dates:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            # 按周分组
            if current_date is None:
                current_date = date_obj
            
            # 计算热度等级（0-4）
            heat_level = int((count / max_count) * 4) if max_count > 0 else 0
            
            # 热度符号
            heat_symbols = ['⬜', '🟩', '🟩', '🟦', '🟧', '🟥']
            heat_symbol = heat_symbols[heat_level] if heat_level < len(heat_symbols) else '🟥'
            
            week_data.append((date_str, heat_symbol, count))
            
            # 每7行输出一组（周）
            if len(week_data) % 7 == 0 or date_str == sorted_dates[-1][0]:
                for d, s, c in week_data:
                    result += f"{s} {d}: {c} 个单词\n"
                if len(week_data) % 7 == 0:
                    result += "-"*60 + "\n"
                week_data = []
        
        # 统计总数
        total_count = sum(daily_stats.values())
        result += "="*60 + "\n"
        result += f"总计: {total_count} 个单词\n"
        result += f"统计天数: {len(daily_stats)} 天\n"
        result += f"平均每天: {total_count/len(daily_stats):.1f} 个\n"
        
        return result
    
    @staticmethod
    def get_word_with_timestamp(words_data: List[Tuple[str, str, Optional[str]]]) -> str:
        """
        获取带时间戳的单词列表
        
        Args:
            words_data: [(单词, 释义, 时间戳), ...] 列表
        
        Returns:
            格式化的单词时间列表
        """
        if not words_data:
            return "暂无单词"
        
        # 按时间戳排序（最新的在前）
        sorted_words = sorted(
            [(w, d, t) for w, d, t in words_data if t],
            key=lambda x: x[2],
            reverse=True
        )
        
        result = "📝 单词加入时间记录\n"
        result += "="*60 + "\n"
        
        for word, definition, timestamp in sorted_words[:100]:  # 显示最新的100个
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                result += f"⏰ {time_str}: {word}\n"
                if definition:
                    result += f"   📌 {definition}\n"
            except Exception:
                pass
        
        if len(sorted_words) > 100:
            result += f"\n... 还有 {len(sorted_words) - 100} 个单词"
        
        return result
    
    @staticmethod
    def get_time_range_statistics(words_data: List[Tuple[str, str, Optional[str]]],
                                   start_date: str = None,
                                   end_date: str = None) -> Tuple[bool, str]:
        """
        获取指定时间范围内的统计
        
        Args:
            words_data: [(单词, 释义, 时间戳), ...] 列表
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
        
        Returns:
            (成功与否, 结果字符串)
        """
        if not words_data:
            return True, "暂无单词数据"
        
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
            end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
            
            filtered_words = []
            for word, definition, timestamp in words_data:
                if timestamp:
                    try:
                        dt = datetime.fromisoformat(timestamp)
                        if (start is None or dt >= start) and (end is None or dt <= end):
                            filtered_words.append((word, definition, timestamp))
                    except Exception:
                        pass
            
            if not filtered_words:
                return True, f"时间范围 {start_date} 到 {end_date} 内无单词"
            
            result = f"📊 时间范围统计: {start_date} 至 {end_date}\n"
            result += f"共 {len(filtered_words)} 个单词:\n\n"
            
            for word, definition, _ in filtered_words[:50]:
                result += f"• {word}: {definition}\n"
            
            if len(filtered_words) > 50:
                result += f"\n... 还有 {len(filtered_words) - 50} 个单词"
            
            return True, result
        
        except ValueError as e:
            return False, f"日期格式错误: {e}，请使用 YYYY-MM-DD 格式"
    
    @staticmethod
    def get_trending_words(words_data: List[Tuple[str, str, Optional[str]]], 
                          days: int = 7) -> str:
        """
        获取最近N天添加的单词
        
        Args:
            words_data: [(单词, 释义, 时间戳), ...] 列表
            days: 天数
        
        Returns:
            结果字符串
        """
        if not words_data:
            return f"暂无过去 {days} 天的单词数据"
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_words = []
        
        for word, definition, timestamp in words_data:
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    if dt >= cutoff_date:
                        recent_words.append((word, definition, timestamp))
                except Exception:
                    pass
        
        if not recent_words:
            return f"过去 {days} 天内无新增单词"
        
        # 按时间排序
        recent_words = sorted(recent_words, key=lambda x: x[2], reverse=True)
        
        result = f"📈 过去 {days} 天的新增单词 (共 {len(recent_words)} 个):\n"
        result += "="*60 + "\n"
        
        for word, definition, timestamp in recent_words[:50]:
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%m-%d %H:%M")
                result += f"• {word:20} ({time_str}): {definition}\n"
            except Exception:
                pass
        
        if len(recent_words) > 50:
            result += f"\n... 还有 {len(recent_words) - 50} 个单词"
        
        return result
