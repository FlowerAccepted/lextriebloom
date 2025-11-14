# 🚀 LextrieBloom 新功能说明

## 📋 已实现的新功能

### 1️⃣ **单词加入时间查询** ⏰
- 每个单词添加时自动记录 ISO 格式的时间戳
- 精确查询时显示单词的加入时间
- 查看单词加入时间记录列表

**相关标签**: 📊 统计分析 → ⏰ 单词加入时间记录

### 2️⃣ **每天加入单词热力图** 📈
- 按日期统计每天加入的单词数量
- 文本形式的热力图展示（使用 Emoji 表示热度等级）
- 显示总计统计、平均每天数量等信息

**相关标签**: 📊 统计分析 → 📈 每日加入热力图

### 3️⃣ **Fail 跳转建议** 💡
- 当查询的单词不在词库中时，系统自动建议相关词缀
- 智能提取单词的前缀和后缀作为潜在词缀
- 检查提议的词缀是否已存在于词缀库中
- 帮助用户快速积累词缀库

**相关标签**: 💡 查询帮助 → ❓ 单词不存在时的建议

**使用场景（ACAM 流程）**:
```
用户查询 "unmistakable" 但词库中不存在
↓
系统建议添加词缀: "un-", "mistake", "able", "tak" 等
↓
用户选择有意义的词缀（如 "un-", "able"）添加到词缀库
↓
下次遇到同样词缀的单词时，系统会识别并分类
```

### 4️⃣ **词缀归类查询** 📚
- 将词库中的单词按照已有词缀自动分类
- 支持前缀和后缀的识别和分类
- 显示每个词缀对应的所有单词

**相关标签**: 📚 词缀分析 → 📊 按词缀分类单词

### 5️⃣ **词缀列表** 🔤
- 完整的词缀库管理
- 按分类（前缀、后缀、中缀、其他）显示
- 显示每个词缀的释义

**相关标签**: 🔤 词缀管理 → 📋 查看所有词缀

### 6️⃣ **词缀释义功能** 📖
- 添加新词缀及其释义
- 查询特定词缀的含义
- 支持多种分类标记

**相关标签**: 🔤 词缀管理 → ➕ 添加词缀 / 🔍 查询词缀释义

---

## 📂 新增文件结构

```
lextriebloom/
├── affix_manager.py          # 词缀管理模块
├── statistics_analyzer.py    # 统计分析模块
├── affixes.json             # 词缀库文件（自动创建）
├── vocabulary.json          # 词库文件（包含时间戳）
├── init_demo.py             # 演示数据初始化脚本
└── ui.py                    # 更新的UI界面（13个标签页）
```

---

## 🎯 使用流程指南

### 场景 1: 从零开始构建词缀库

1. **运行初始化脚本**
   ```bash
   python3 init_demo.py
   ```
   会生成 42 个演示单词（包含多个词缀），分布在 14 天内

2. **查看热力图统计**
   - 打开 `📊 统计分析` 标签
   - 点击 `📈 生成热力图` 查看每日统计

3. **检测潜在词缀**
   - 打开 `📚 词缀分析` 标签
   - 点击 `🔍 检测` 自动检测高频词缀

4. **添加词缀**
   - 打开 `🔤 词缀管理` 标签
   - 输入词缀（如 "un-"）、释义和分类
   - 点击 `➕ 添加词缀`

5. **查看分类结果**
   - 打开 `📚 词缀分析` 标签
   - 点击 `📊 分析分类` 查看单词按词缀的分布

### 场景 2: 使用 Fail 跳转建议（ACAM流程）

1. **查询不存在的单词**
   - 打开 `💡 查询帮助` 标签
   - 输入词库中没有的单词（如 "unpredictable"）
   - 点击 `❓ 获取建议`

2. **系统显示建议词缀**
   系统会建议：
   - 已存在的词缀（✓）
   - 可添加的新词缀（✗）

3. **添加新词缀**
   - 根据建议，前往 `🔤 词缀管理` 标签
   - 添加推荐的新词缀

### 场景 3: 时间范围统计

1. **打开统计分析标签**
   - `📊 统计分析` → `📅 时间范围查询`

2. **输入日期范围**
   - 开始日期：YYYY-MM-DD 格式
   - 结束日期：YYYY-MM-DD 格式

3. **查看该范围内的单词**

---

## 🔧 API 和类说明

### AffixManager (affix_manager.py)

```python
# 初始化
affix_mgr = AffixManager("affixes.json")

# 添加词缀
success, msg = affix_mgr.add_affix("un-", "表示否定或相反", "前缀")

# 查询词缀定义
success, msg = affix_mgr.get_affix_definition("un-")

# 列出所有词缀
success, msg = affix_mgr.list_all_affixes()

# 按词缀分类单词
categorized = affix_mgr.categorize_words([("unbelievable", "难以置信的"), ...])

# 检测潜在词缀
potential = affix_mgr.extract_potential_affixes(["unbelievable", "unable", ...])

# 提取差异部分（Fail跳转用）
parts = affix_mgr.extract_difference_parts("unpredictable")
```

### StatisticsAnalyzer (statistics_analyzer.py)

```python
# 初始化
analyzer = StatisticsAnalyzer()

# 每日统计
daily_stats = analyzer.get_daily_statistics(words_data)

# 生成热力图文本
heatmap = analyzer.generate_heatmap_text(daily_stats)

# 获取单词时间戳
timestamp_list = analyzer.get_word_with_timestamp(words_data)

# 最近N天
trending = analyzer.get_trending_words(words_data, days=7)

# 时间范围查询
success, msg = analyzer.get_time_range_statistics(words_data, "2025-11-01", "2025-11-14")
```

### Trie 数据结构更新

```python
# 现在支持时间戳
trie.insert(word, definition, timestamp)

# search 返回三元组
exists, definition, timestamp = trie.search(word)

# get_all_words 返回三元组列表
words_data = trie.get_all_words()  # [(word, def, ts), ...]
```

---

## 📊 数据格式

### vocabulary.json（更新）
```json
{
  "words": [
    {
      "word": "unbelievable",
      "definition": "难以置信的",
      "timestamp": "2025-11-10T08:44:08.871831"
    },
    ...
  ]
}
```

### affixes.json（新增）
```json
{
  "un-": {
    "definition": "表示否定或相反",
    "category": "前缀",
    "related_words": []
  },
  ...
}
```

---

## ✨ 功能特色

- 📅 **时间追踪**: 每个单词记录确切的加入时间
- 🔥 **热力统计**: 可视化每日学习进度
- 🧬 **词缀智能**: 自动检测和推荐词缀
- 💡 **智能建议**: Fail跳转时给出可行的词缀建议
- 🎯 **分类管理**: 自动按词缀分类单词，形成知识体系
- 🔄 **持久化**: 所有数据（单词、词缀、时间戳）都自动保存

---

## 🚀 快速开始

1. **首次运行 - 初始化演示数据**
   ```bash
   python3 init_demo.py
   python main.py
   ```

2. **已有数据 - 直接启动**
   ```bash
   python main.py
   ```

3. **浏览新功能**
   - 打开浏览器访问 http://127.0.0.1:7860
   - 依次尝试 13 个标签页的新功能

---

## 📝 备注

- 所有时间戳都使用 ISO 8601 格式（本地时区）
- 词缀库独立保存到 `affixes.json`
- 时间范围查询支持开放式范围（只指定开始或结束日期）
- 热力图自动计算最高频率并标准化热度等级

---

**祝学习愉快！🎉**
