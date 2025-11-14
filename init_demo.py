#!/usr/bin/env python3
"""
初始化脚本 - 用于添加测试数据和演示新功能
"""

from vocabulary_manager import VocabularyManager, JSONStorage
from affix_manager import AffixManager
from datetime import datetime, timedelta
import json

def init_demo_data():
    """初始化演示数据"""
    
    manager = VocabularyManager(storage_backend=JSONStorage())
    
    # 添加一些测试单词，涵盖多个词缀
    demo_words = [
        ("unbelievable", "难以置信的"),
        ("unable", "无法的"),
        ("unforgettable", "难以遗忘的"),
        ("unnecessary", "不必要的"),
        ("rewrite", "重写"),
        ("rebuild", "重建"),
        ("reconsider", "重新考虑"),
        ("redo", "重做"),
        ("disable", "禁用"),
        ("disconnect", "断开连接"),
        ("dislike", "不喜欢"),
        ("distrust", "不信任"),
        ("preview", "预览"),
        ("prepare", "准备"),
        ("presume", "假设"),
        ("prevention", "预防"),
        ("action", "行动"),
        ("creation", "创造"),
        ("nation", "国家"),
        ("station", "车站"),
        ("running", "运行"),
        ("walking", "走路"),
        ("talking", "说话"),
        ("playing", "玩耍"),
        ("quickly", "快速地"),
        ("slowly", "缓慢地"),
        ("carefully", "小心地"),
        ("happily", "快乐地"),
        ("happiness", "幸福"),
        ("sadness", "悲伤"),
        ("goodness", "善良"),
        ("darkness", "黑暗"),
        ("reasonable", "合理的"),
        ("comfortable", "舒适的"),
        ("possible", "可能的"),
        ("beautiful", "美丽的"),
        ("powerful", "强大的"),
        ("helpful", "有帮助的"),
        ("homeless", "无家可归的"),
        ("hopeless", "无望的"),
        ("useless", "无用的"),
        ("worthless", "无价值的"),
    ]
    
    # 根据时间均匀分布这些单词在过去14天内
    base_date = datetime.now() - timedelta(days=13)  # 从13天前开始
    
    for idx, (word, definition) in enumerate(demo_words):
        # 计算时间戳：每2-3个单词分配到一天
        day_offset = idx // 3  # 每3个单词为一天
        hour_offset = (idx % 3) * 7  # 一天内分3个时间段
        minute_offset = (idx % 60) * 2  # 分钟偏移
        
        word_date = base_date + timedelta(days=day_offset, hours=hour_offset, minutes=minute_offset)
        timestamp = word_date.isoformat()
        
        # 添加单词
        manager.trie.insert(word, definition, timestamp)
    
    # 保存
    manager.save("vocabulary.json")
    print(f"✅ 成功初始化 {len(demo_words)} 个演示单词")
    
    # 打印一些信息
    words_data = manager.get_all_words_with_timestamp()
    print(f"📊 词库状态:")
    print(f"  - 总单词数: {len(words_data)}")
    if words_data:
        first = words_data[0]
        last = words_data[-1]
        print(f"  - 首个单词: {first[0]} ({first[2][:10]})")
        print(f"  - 最新单词: {last[0]} ({last[2][:10]})")


if __name__ == "__main__":
    init_demo_data()
    print("\n✅ 演示数据已初始化完成！")
    print("📖 建议操作:")
    print("  1. 打开\"📊 统计分析\"标签查看热力图")
    print("  2. 打开\"🔤 词缀管理\"标签添加或管理词缀")
    print("  3. 打开\"📚 词缀分析\"标签查看单词分类")
    print("  4. 打开\"💡 查询帮助\"标签测试Fail跳转建议")
