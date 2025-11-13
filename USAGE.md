# 📚 单词积累本 - 快速使用指南

## 🚀 启动应用

### 方式1: 使用shell脚本（推荐）
```bash
chmod +x run.sh
./run.sh
```

### 方式2: 直接运行Python
```bash
# 首先安装依赖
pip install -r requirements.txt

# 运行应用
python main.py
```

应用启动后，会在浏览器中打开 `http://127.0.0.1:7860`

## 📖 功能使用说明

### ➕ 添加单条单词

1. 进入"添加单词"页签
2. 在"单词"框输入英文单词（例如：apple）
3. 在"释义"框输入中文解释（例如：苹果）
4. 点击"➕ 添加"按钮

**示例**:
```
单词: python
释义: Python编程语言，一种高级编程语言
```

### 📤 批量导入单词

1. 进入"导入文件"页签
2. 准备txt文件，格式为 `单词 空格 释义`
3. 上传文件
4. 点击"📤 导入"按钮

**文件内容示例** (保存为 words.txt):
```
# 动物类单词
cat 猫
dog 狗
elephant 大象

# 食物类单词
apple 苹果
banana 香蕉
```

**支持的特性**:
- ✅ 注释行（以#开头）
- ✅ 空行
- ✅ 多个词义（用逗号分隔）
- ✅ 自动处理重复单词（更新释义）

### 🔍 精确查询

1. 进入"精确查询"页签
2. 输入要查询的单词
3. 点击"🔍 查询"按钮

**示例**:
```
输入: apple
输出: 
单词: apple
释义: 苹果
```

### 🔎 前缀查询

1. 进入"前缀查询"页签
2. 输入前缀（例如：app）
3. 点击"🔎 查询"按钮
4. 查看所有以该前缀开头的单词（已按字典序排列）

**示例**:
```
输入: app
输出:
找到 3 个单词:
• apple: 苹果
• application: 应用程序
• apply: 应用，申请
```

**常用查询**:
- `s` - 查询所有以s开头的单词
- `un` - 查询所有以un开头的单词（如unbelievable）
- `pre` - 查询所有以pre开头的单词（如prepare）

### 📋 查看所有单词

1. 进入"查看所有"页签
2. 点击"📋 刷新列表"按钮
3. 查看所有单词（已按字典序排列）

**提示**: 如果单词很多，界面会显示前100个，剩余数量会提示

### 🗑️ 删除单词

1. 进入"删除单词"页签
2. 输入要删除的单词
3. 点击"🗑️ 删除"按钮

**示例**:
```
输入: apple
输出: 单词 'apple' 删除成功
```

### 💾 数据管理

#### 📊 查看统计信息
1. 进入"数据管理"页签
2. 点击"📊 刷新统计"按钮
3. 查看：
   - 总单词数
   - 存储类型

#### 💾 保存数据
1. 在"保存路径"输入框输入文件路径（例如：vocabulary.json）
2. 点击"💾 保存"按钮
3. 数据会保存为JSON格式

**自动保存**: 每次添加/删除/修改单词后，都会自动保存到 `vocabulary.json`

#### 📂 加载数据
1. 在"加载路径"输入框输入文件路径（例如：vocabulary.json）
2. 点击"📂 加载"按钮
3. 之前保存的单词将被加载

#### 📤 导出数据
1. 在"导出路径"输入框输入导出文件名
2. 选择导出格式：
   - **TXT**: 纯文本格式，可直接查看编辑
   - **JSON**: 结构化格式，便于程序处理
   - **CSV**: 表格格式，可用Excel打开
3. 点击"📤 导出"按钮

**导出格式示例**:

TXT格式:
```
apple 苹果
book 书籍
cat 猫
```

JSON格式:
```json
{
  "words": [
    {"word": "apple", "definition": "苹果"},
    {"word": "book", "definition": "书籍"}
  ]
}
```

CSV格式:
```
word,definition
apple,苹果
book,书籍
```

## 💡 使用技巧

### 技巧1: 快速导入大量单词
1. 准备txt文件，每行 `单词 释义`
2. 通过"导入文件"一次性导入
3. 比逐个添加快100倍！

### 技巧2: 定期备份
```bash
# 备份当前词库
cp vocabulary.json vocabulary_backup_$(date +%Y%m%d).json
```

### 技巧3: 前缀查询学习词族
比如输入 "un" 可以查看所有以"un"开头的单词（usually, understand, unexpected等），学习词根的用法。

### 技巧4: 导出后使用Excel
1. 导出为CSV格式
2. 用Excel打开
3. 可以进行高级筛选、排序、统计
4. 方便打印学习

### 技巧5: 多个词库管理
```bash
# 创建不同主题的词库
python main.py  # 打开默认vocabulary.json

# 修改代码或手动保存为不同文件
# vocabulary_business.json - 商务英语
# vocabulary_technical.json - 技术英语
# vocabulary_daily.json - 日常用语
```

## 🔄 工作流示例

### 场景1: 学习每日单词
```
1. 早上打开应用
2. 通过"精确查询"复习昨天的单词
3. 通过"添加单词"页签添加今天的3个新单词
4. 晚上用"前缀查询"复习相关词族
5. 应用自动保存
```

### 场景2: 整理学习资料
```
1. 从课本或网络收集单词，保存为txt文件
2. 格式化为 "单词 释义" 的形式
3. 使用"导入文件"导入到应用
4. 用"查看所有"查看完整列表
5. 用"前缀查询"按主题学习
6. 导出为CSV在Excel中统计分析
```

### 场景3: 考试准备
```
1. 导入常考词汇
2. 每天通过"前缀查询"学习词族
3. 定期导出到Excel进行统计测试
4. 备份重要词库
5. 考前快速浏览"查看所有"
```

## ⚙️ 常见问题

**Q: 数据存储在哪里？**
A: 默认存储在 `vocabulary.json`，与 `main.py` 同一目录。

**Q: 可以导入其他格式的文件吗？**
A: 目前仅支持txt格式。其他格式需要先转换。

**Q: 单词删除后可以恢复吗？**
A: 可以！在删除前，可以导出备份，需要时重新导入。

**Q: 支持多少个单词？**
A: 理论上无限制，但性能最优在10万个单词以下。

**Q: 可以导出后修改再导入吗？**
A: 可以！txt和json格式都支持手动编辑后重新导入。

**Q: 如何清空所有单词？**
A: 最简单的方法是删除 `vocabulary.json` 文件。

## 🔧 使用API进行自动化

如果要在Python程序中使用词库：

```python
from vocabulary_manager import VocabularyManager, JSONStorage

# 创建管理器
manager = VocabularyManager(storage_backend=JSONStorage())

# 加载已保存的词库
manager.load("vocabulary.json")

# 查询单词
exists, definition = manager.trie.search("apple")
if exists:
    print(f"apple: {definition}")

# 获取所有单词
all_words = manager.trie.get_all_words()
for word, definition in all_words:
    print(f"{word}: {definition}")

# 前缀查询
results = manager.trie.prefix_search("app")
for word, definition in results:
    print(f"{word}: {definition}")

# 添加新单词
manager.add_word("python", "Python编程语言")

# 保存
manager.save("vocabulary.json")
```

## 📞 获取帮助

- 查看应用内的"❓ 帮助"页签
- 阅读 README.md 了解项目信息
- 查看 ARCHITECTURE.md 了解技术细节
- 运行 test_demo.py 查看功能演示

祝你学习愉快！📚✨
