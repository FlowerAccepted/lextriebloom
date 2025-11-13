# 📚 单词积累本 (LexTrieBloom)

基于Trie数据结构的高效单词管理工具，提供友好的Gradio交互界面。

## ✨ 功能特性

- ⚡ **高效存储**: 使用Trie数据结构，O(m)时间复杂度查询，其中m为单词长度
- 📝 **单条导入**: 输入单词和释义，实时添加
- 📤 **批量导入**: 支持txt文件导入，格式：`单词 释义`
- 🔍 **精确查询**: 查询单词及其释义
- 🔎 **前缀查询**: 查询所有以某前缀开头的单词，结果自动按字典序排列
- 📋 **全部列表**: 查看所有单词，按字典序排序
- 🗑️ **删除单词**: 删除指定单词
- 💾 **灵活存储**: 支持JSON和Pickle格式
- 📥📤 **导入导出**: 支持多种格式（TXT、JSON、CSV）
- 🔧 **易于扩展**: 模块化设计，便于添加新功能

## 📁 项目结构

```
lextriebloom/
├── main.py                 # 主程序入口
├── trie.py                 # Trie数据结构实现
├── vocabulary_manager.py   # 单词管理器（支持多种存储后端）
├── ui.py                   # Gradio交互界面
├── requirements.txt        # 依赖包列表
└── README.md              # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python main.py
```

然后在浏览器中打开 `http://127.0.0.1:7860`

## 📖 使用说明

### ➕ 添加单词
1. 切换到"添加单词"页签
2. 输入单词和释义
3. 点击"➕ 添加"按钮

### 📤 导入文件
1. 切换到"导入文件"页签
2. 上传txt文件
3. 点击"📤 导入"按钮

**文件格式示例**:
```
# 注释行以#开头
apple 苹果
book 书籍
cat 猫
dog 狗
```

### 🔍 精确查询
1. 切换到"精确查询"页签
2. 输入要查询的单词
3. 点击"🔍 查询"按钮

### 🔎 前缀查询
1. 切换到"前缀查询"页签
2. 输入前缀（例如 "app" 会找到 "apple", "application" 等）
3. 点击"🔎 查询"按钮
4. 结果会自动按字典序排列

### 📋 查看所有
1. 切换到"查看所有"页签
2. 点击"📋 刷新列表"按钮
3. 所有单词会按字典序显示

### 🗑️ 删除单词
1. 切换到"删除单词"页签
2. 输入要删除的单词
3. 点击"🗑️ 删除"按钮

### 💾 数据管理

#### 保存/加载
- 自动保存到 `vocabulary.json`
- 支持自定义保存位置
- 支持从任何保存的文件加载

#### 导出数据
- **TXT格式**: 纯文本，每行 `单词 释义`
- **JSON格式**: 结构化格式，便于其他工具处理
- **CSV格式**: 电子表格格式，可用Excel打开

## 🔧 扩展性设计

### 添加新的存储后端

```python
from vocabulary_manager import StorageBackend

class MyStorage(StorageBackend):
    def save(self, trie, filepath):
        # 实现保存逻辑
        pass
    
    def load(self, filepath):
        # 实现加载逻辑
        pass

# 使用新的存储后端
manager = VocabularyManager(storage_backend=MyStorage())
```

### 添加新功能到Trie

```python
from trie import Trie

class EnhancedTrie(Trie):
    def fuzzy_search(self, word):
        # 实现模糊查询
        pass
    
    def get_word_stats(self):
        # 实现统计功能
        pass
```

### 扩展UI界面

在 `ui.py` 中的 `VocabularyUI` 类中添加新的回调函数和页签即可。

## 💡 使用示例

### Python API使用

```python
from vocabulary_manager import VocabularyManager, JSONStorage

# 创建管理器
manager = VocabularyManager(storage_backend=JSONStorage())

# 添加单词
manager.add_word("apple", "苹果")
manager.add_word("book", "书籍")

# 查询单词
exists, definition = manager.trie.search("apple")

# 前缀查询
words = manager.trie.prefix_search("app")

# 获取所有单词
all_words = manager.trie.get_all_words()

# 保存
manager.save("my_vocabulary.json")

# 加载
manager.load("my_vocabulary.json")
```

## 📊 性能特性

- **查询**: O(m)，m为单词长度
- **插入**: O(m)，m为单词长度
- **删除**: O(m)，m为单词长度
- **前缀查询**: O(n)，n为结果数量
- **内存**: 与单词总数和长度成正比

## 🎯 后续可扩展方向

1. **音频发音**: 添加单词发音功能
2. **例句示例**: 为每个单词添加使用例句
3. **分类管理**: 支持为单词添加标签和分类
4. **学习进度**: 记录单词学习进度
5. **云同步**: 支持云存储同步
6. **移动应用**: 使用Flutter/React Native开发移动版
7. **AI增强**: 集成LLM生成更好的释义和例句
8. **导入导出增强**: 支持导入导出到其他流行词典格式（如DICT、STARDICT）
9. **全文搜索**: 在释义中搜索
10. **单词关联**: 支持单词关联和同义词

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 联系方式

如有问题或建议，欢迎提出！
