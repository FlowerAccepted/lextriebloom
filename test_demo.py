"""
单词积累本的测试脚本
演示如何使用VocabularyManager API
"""

from vocabulary_manager import VocabularyManager, JSONStorage, PickleStorage
from trie import Trie


def test_basic_operations():
    """测试基本操作"""
    print("=" * 50)
    print("测试1: 基本操作")
    print("=" * 50)
    
    manager = VocabularyManager(storage_backend=JSONStorage())
    
    # 添加单词
    print("\n➕ 添加单词:")
    print(manager.add_word("apple", "苹果")[1])
    print(manager.add_word("book", "书籍")[1])
    print(manager.add_word("cat", "猫")[1])
    
    # 查询单词
    print("\n🔍 查询单词 'apple':")
    success, result = manager.search_word("apple")
    print(result)
    
    # 前缀查询
    print("\n🔎 前缀查询 'a':")
    success, result = manager.prefix_search("a")
    print(result)
    
    # 获取所有单词
    print("\n📋 所有单词:")
    success, result = manager.list_all_words()
    print(result)
    
    return manager


def test_file_operations(manager):
    """测试文件操作"""
    print("\n" + "=" * 50)
    print("测试2: 文件操作")
    print("=" * 50)
    
    # 导入文件
    print("\n📤 从sample_words.txt导入:")
    success, msg = manager.import_from_file("sample_words.txt")
    print(msg)
    
    # 统计信息
    print("\n📊 统计信息:")
    stats = manager.get_stats()
    print(f"总单词数: {stats['total_words']}")
    print(f"存储类型: {stats['storage_type']}")


def test_storage_operations(manager):
    """测试存储操作"""
    print("\n" + "=" * 50)
    print("测试3: 存储操作")
    print("=" * 50)
    
    # 保存为JSON
    print("\n💾 保存为JSON:")
    success, msg = manager.save("test_vocabulary.json")
    print(msg)
    
    # 保存为Pickle
    print("\n💾 保存为Pickle:")
    manager_pickle = VocabularyManager(storage_backend=PickleStorage())
    success, msg = manager_pickle.import_from_file("sample_words.txt")
    print(msg)
    success, msg = manager_pickle.save("test_vocabulary.pkl")
    print(msg)
    
    # 导出为不同格式
    print("\n📤 导出为不同格式:")
    print(manager.export_to_file("test_export.txt", "txt")[1])
    print(manager.export_to_file("test_export.json", "json")[1])
    print(manager.export_to_file("test_export.csv", "csv")[1])


def test_search_operations(manager):
    """测试查询操作"""
    print("\n" + "=" * 50)
    print("测试4: 高级查询")
    print("=" * 50)
    
    print("\n🔎 前缀查询 'app':")
    success, result = manager.prefix_search("app")
    print(result)
    
    print("\n🔎 前缀查询 'pro':")
    success, result = manager.prefix_search("pro")
    print(result)
    
    print("\n🔎 前缀查询 's':")
    success, result = manager.prefix_search("s")
    print(result)


def test_delete_operations(manager):
    """测试删除操作"""
    print("\n" + "=" * 50)
    print("测试5: 删除操作")
    print("=" * 50)
    
    print("\n🗑️ 删除单词 'apple':")
    success, msg = manager.delete_word("apple")
    print(msg)
    
    print("\n🔍 查询已删除的单词:")
    success, result = manager.search_word("apple")
    print(result)
    
    print("\n📊 更新后的统计:")
    stats = manager.get_stats()
    print(f"总单词数: {stats['total_words']}")


def test_trie_performance():
    """测试Trie的性能"""
    print("\n" + "=" * 50)
    print("测试6: Trie性能测试")
    print("=" * 50)
    
    import time
    
    trie = Trie()
    
    # 生成测试数据
    test_words = [
        ("apple", "苹果"),
        ("application", "应用"),
        ("apply", "申请"),
        ("apt", "恰当的"),
        ("banana", "香蕉"),
        ("bank", "银行"),
        ("base", "基地"),
        ("basic", "基本的"),
        ("bat", "蝙蝠"),
        ("beach", "海滩"),
    ]
    
    # 测试插入性能
    print("\n⏱️ 测试插入性能:")
    start = time.time()
    for word, definition in test_words * 100:  # 插入1000个单词
        trie.insert(word, definition)
    end = time.time()
    print(f"插入1000个单词耗时: {end - start:.4f}秒")
    
    # 测试查询性能
    print("\n⏱️ 测试查询性能:")
    start = time.time()
    for _ in range(1000):
        trie.search("apple")
    end = time.time()
    print(f"1000次查询耗时: {end - start:.4f}秒")
    
    # 测试前缀查询性能
    print("\n⏱️ 测试前缀查询性能:")
    start = time.time()
    for _ in range(1000):
        trie.prefix_search("app")
    end = time.time()
    print(f"1000次前缀查询耗时: {end - start:.4f}秒")


def main():
    """主测试函数"""
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " " * 10 + "📚 单词积累本 - 功能测试" + " " * 14 + "║")
    print("╚" + "=" * 48 + "╝")
    
    # 运行所有测试
    manager = test_basic_operations()
    test_file_operations(manager)
    test_storage_operations(manager)
    test_search_operations(manager)
    test_delete_operations(manager)
    test_trie_performance()
    
    print("\n" + "=" * 50)
    print("✅ 所有测试完成！")
    print("=" * 50)
    print("\n📝 生成的文件:")
    print("  - test_vocabulary.json")
    print("  - test_vocabulary.pkl")
    print("  - test_export.txt")
    print("  - test_export.json")
    print("  - test_export.csv")


if __name__ == "__main__":
    main()
