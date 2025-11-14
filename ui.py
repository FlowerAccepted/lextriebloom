"""
使用Gradio构建的交互式用户界面
"""

import gradio as gr
from vocabulary_manager import VocabularyManager, JSONStorage, PickleStorage
from affix_manager import AffixManager
from statistics_analyzer import StatisticsAnalyzer
from pathlib import Path
import settings_manager


class VocabularyUI:
    """单词积累本的Gradio用户界面"""
    
    def __init__(self):
        self.manager = VocabularyManager(storage_backend=JSONStorage())
        self.affix_manager = AffixManager(storage_path="affixes.json")
        self.stats_analyzer = StatisticsAnalyzer()
        self.default_save_path = "vocabulary.json"
        self.font_size = 16  # 默认字体大小
        
        # 字体设置
        self.en_font = "Arial"  # 英文字体
        self.zh_font = "SimHei"  # 中文字体
        self.font_style = "normal"  # 字体样式
        
        # 主题设置（使用主题类）
        self.theme = "soft"  # 当前主题
        # 使用主题类而不是实例或工厂，兼容 Gradio 对 Theme 的要求（theme 应为 class）
        self.themes_dict = {
            "soft": gr.themes.Soft,
            "default": gr.themes.Default,
            "monochrome": gr.themes.Monochrome,
            "glass": gr.themes.Glass,
            # 额外预设（可按需扩展）
            "solarized": gr.themes.Default,
            "midnight": gr.themes.Monochrome,
            "pastel": gr.themes.Soft
        }
        
        # 为主题添加中英文标签（用于 UI 下拉框）
        self.theme_labels = {
            "soft": "🌤️ 柔和",
            "default": "🎨 默认",
            "monochrome": "⚫ 单色",
            "glass": "🏔️ 玻璃",
            "solarized": "🌅 Solarized",
            "midnight": "🌙 午夜",
            "pastel": "🎀 Pastel"
        }
        
        # 主题实例缓存（在 __init__ 中预先创建）
        self.theme_instances = {}
        for theme_name, theme_class in self.themes_dict.items():
            try:
                self.theme_instances[theme_name] = theme_class()
            except Exception:
                self.theme_instances[theme_name] = gr.themes.Default()
        
        # 尝试从 settings.json 加载用户设置
        s = settings_manager.load_settings()
        if s:
            self.font_size = s.get("font_size", self.font_size)
            self.en_font = s.get("en_font", self.en_font)
            self.zh_font = s.get("zh_font", self.zh_font)
            self.font_style = s.get("font_style", self.font_style)
            self.theme = s.get("theme", self.theme)

        self.load_saved_data()
    
    def load_saved_data(self):
        """启动时加载保存的数据"""
        if Path(self.default_save_path).exists():
            success, msg = self.manager.load(self.default_save_path)
            print(msg)
    
    def add_single_word(self, word: str, definition: str) -> str:
        """添加单条单词的回调函数"""
        success, msg = self.manager.add_word(word, definition)
        if success:
            self._auto_save()
        return msg
    
    def import_file(self, file_obj) -> str:
        """导入文件的回调函数"""
        if file_obj is None:
            return "请选择要导入的文件"
        
        try:
            # 处理gradio上传的文件
            filepath = file_obj.name if hasattr(file_obj, 'name') else str(file_obj)
            success, msg = self.manager.import_from_file(filepath)
            if success:
                self._auto_save()
            return msg
        except Exception as e:
            return f"导入失败: {e}"
    
    def search_word_ui(self, word: str) -> str:
        """查询单词的回调函数"""
        _, result, timestamp = self.manager.search_word(word)
        return result
    
    def prefix_search_ui(self, prefix: str) -> str:
        """前缀查询的回调函数"""
        _, result = self.manager.prefix_search(prefix)
        return result
    
    def list_all_ui(self) -> str:
        """列出所有单词的回调函数"""
        _, result = self.manager.list_all_words()
        return result
    
    def delete_word_ui(self, word: str) -> str:
        """删除单词的回调函数"""
        success, msg = self.manager.delete_word(word)
        if success:
            self._auto_save()
        return msg
    
    def get_stats_ui(self) -> str:
        """获取统计信息的回调函数"""
        stats = self.manager.get_stats()
        return f"📊 统计信息:\n总单词数: {stats['total_words']}\n存储类型: {stats['storage_type']}"
    
    def save_to_file_ui(self, filepath: str) -> str:
        """保存到文件的回调函数"""
        if not filepath.strip():
            filepath = self.default_save_path
        
        success, msg = self.manager.save(filepath)
        return msg
    
    def load_from_file_ui(self, filepath: str) -> str:
        """从文件加载的回调函数"""
        if not filepath.strip():
            filepath = self.default_save_path
        
        success, msg = self.manager.load(filepath)
        return msg
    
    def export_file_ui(self, filepath: str, export_format: str) -> str:
        """导出到文件的回调函数"""
        if not filepath.strip():
            filepath = f"vocabulary_export.{export_format}"
        
        success, msg = self.manager.export_to_file(filepath, export_format)
        return msg
    
    def delete_all_data_ui(self) -> str:
        """清除所有数据的回调函数"""
        try:
            # 重新初始化Trie
            self.manager.trie = type(self.manager.trie)()
            # 删除保存的文件
            import os
            if os.path.exists(self.default_save_path):
                os.remove(self.default_save_path)
            return "✅ 所有数据已清除！词库已重置。"
        except Exception as e:
            return f"❌ 清除数据失败: {e}"
    
    def set_font_size(self, size: int) -> tuple:
        """设置字体倍率的回调函数，返回 (消息, CSS HTML)"""
        try:
            # size 现在是倍率百分比（例如 100 = 1.0x, 150 = 1.5x）
            self.font_size = max(80, min(size, 150))  # 限制范围 80%-150%
            # 保存设置
            settings_manager.save_settings({
                "font_size": self.font_size,
                "en_font": getattr(self, 'en_font', 'Arial'),
                "zh_font": getattr(self, 'zh_font', 'SimHei'),
                "font_style": getattr(self, 'font_style', 'normal'),
                "theme": getattr(self, 'theme', 'soft')
            })
            msg = f"✅ 字体倍率已设置为 {self.font_size}%"
            css = self.make_css_html()
            return msg, css
        except Exception as e:
            return f"❌ 设置失败: {e}", self.make_css_html()
    
    def set_fonts(self, en_font: str, zh_font: str) -> tuple:
        """设置英文和中文字体的回调函数，返回 (消息, CSS HTML)"""
        try:
            self.en_font = en_font if en_font.strip() else "Arial"
            self.zh_font = zh_font if zh_font.strip() else "SimHei"
            settings_manager.save_settings({
                "font_size": getattr(self, 'font_size', 16),
                "en_font": self.en_font,
                "zh_font": self.zh_font,
                "font_style": getattr(self, 'font_style', 'normal'),
                "theme": getattr(self, 'theme', 'soft')
            })
            msg = f"✅ 英文字体: {self.en_font}\n✅ 中文字体: {self.zh_font}"
            css = self.make_css_html()
            return msg, css
        except Exception as e:
            return f"❌ 设置失败: {e}", self.make_css_html()
    
    def set_font_style(self, style: str) -> tuple:
        """设置字体样式的回调函数，返回 (消息, CSS HTML)"""
        try:
            self.font_style = style
            style_names = {
                "normal": "正常",
                "italic": "斜体",
                "bold": "加粗",
                "bold-italic": "加粗斜体"
            }
            settings_manager.save_settings({
                "font_size": getattr(self, 'font_size', 16),
                "en_font": getattr(self, 'en_font', 'Arial'),
                "zh_font": getattr(self, 'zh_font', 'SimHei'),
                "font_style": self.font_style,
                "theme": getattr(self, 'theme', 'soft')
            })
            msg = f"✅ 字体样式已设置为: {style_names.get(style, style)}"
            css = self.make_css_html()
            return msg, css
        except Exception as e:
            return f"❌ 设置失败: {e}", self.make_css_html()
    
    def set_theme(self, theme_name: str) -> tuple:
        """设置主题的回调函数，返回 (消息, HTML/JS 脚本)"""
        try:
            if theme_name in self.themes_dict:
                self.theme = theme_name
                settings_manager.save_settings({
                    "font_size": getattr(self, 'font_size', 16),
                    "en_font": getattr(self, 'en_font', 'Arial'),
                    "zh_font": getattr(self, 'zh_font', 'SimHei'),
                    "font_style": getattr(self, 'font_style', 'normal'),
                    "theme": self.theme
                })
                msg = f"✅ 主题已切换为: {self.theme_labels.get(theme_name, theme_name)}"
                # 返回自动刷新页面的 JavaScript
                refresh_js = """
<script>
setTimeout(function() {
  location.reload();
}, 500);
</script>
"""
                return msg, refresh_js
            else:
                return "❌ 主题不存在", ""
        except Exception as e:
            return f"❌ 设置失败: {e}", ""
    
    # ============ 词缀管理相关回调方法 ============
    
    def add_affix_ui(self, affix: str, definition: str, category: str) -> str:
        """添加词缀的回调函数"""
        success, msg = self.affix_manager.add_affix(affix, definition, category)
        return msg
    
    def query_affix_definition_ui(self, affix: str) -> str:
        """查询词缀释义的回调函数"""
        success, msg = self.affix_manager.get_affix_definition(affix)
        return msg
    
    def list_all_affixes_ui(self) -> str:
        """列出所有词缀的回调函数"""
        success, msg = self.affix_manager.list_all_affixes()
        return msg
    
    def categorize_words_by_affix_ui(self) -> str:
        """按词缀分类单词的回调函数"""
        words_data = self.manager.get_all_words_with_timestamp()
        words = [(w, d) for w, d, _ in words_data]
        categorized = self.affix_manager.categorize_words(words)
        
        result = "📚 单词按词缀分类\n"
        result += "="*60 + "\n\n"
        
        for affix, words_list in sorted(categorized.items()):
            result += f"【{affix}】 ({len(words_list)} 个)\n"
            for word, definition in words_list[:20]:
                result += f"  • {word}: {definition}\n"
            if len(words_list) > 20:
                result += f"  ... 还有 {len(words_list) - 20} 个\n"
            result += "\n"
        
        return result
    
    def detect_affixes_ui(self) -> str:
        """检测潜在词缀的回调函数"""
        words_data = self.manager.get_all_words_with_timestamp()
        words = [w for w, _, _ in words_data]
        potential = self.affix_manager.extract_potential_affixes(words)
        
        if not potential:
            return "未检测到潜在词缀（需要更多数据）"
        
        result = "🔍 检测到的潜在词缀\n"
        result += "="*60 + "\n"
        result += "这些词缀可能值得添加到词缀库中:\n\n"
        
        for affix, count in sorted(potential.items(), key=lambda x: -x[1]):
            result += f"• {affix}: 出现 {count} 次\n"
        
        return result
    
    # ============ 统计分析相关回调方法 ============
    
    def get_daily_statistics_ui(self) -> str:
        """获取每日统计的回调函数"""
        words_data = self.manager.get_all_words_with_timestamp()
        daily_stats = self.stats_analyzer.get_daily_statistics(words_data)
        heatmap = self.stats_analyzer.generate_heatmap_text(daily_stats)
        return heatmap
    
    def get_word_timestamps_ui(self) -> str:
        """获取单词加入时间的回调函数"""
        words_data = self.manager.get_all_words_with_timestamp()
        result = self.stats_analyzer.get_word_with_timestamp(words_data)
        return result
    
    def get_trending_words_ui(self, days: int = 7) -> str:
        """获取最近N天的热门单词的回调函数"""
        words_data = self.manager.get_all_words_with_timestamp()
        result = self.stats_analyzer.get_trending_words(words_data, int(days))
        return result
    
    def query_time_range_ui(self, start_date: str, end_date: str) -> str:
        """查询时间范围内的单词的回调函数"""
        words_data = self.manager.get_all_words_with_timestamp()
        success, msg = self.stats_analyzer.get_time_range_statistics(
            words_data, start_date, end_date
        )
        return msg
    
    def fail_jump_affix_suggestion_ui(self, word: str) -> str:
        """Fail跳转 - 建议将差异部分存入词缀的回调函数"""
        # 查询单词是否存在
        exists, _, _ = self.manager.search_word(word)
        
        if exists:
            return f"✅ 单词 '{word}' 已在词库中"
        
        # 单词不存在，提取可能的词缀并建议
        potential_parts = self.affix_manager.extract_difference_parts(word)
        
        result = f"❌ 单词 '{word}' 不在词库中\n\n"
        result += "💡 您可能想要将这些部分存入词缀库:\n"
        result += "="*60 + "\n"
        
        for part in potential_parts[:5]:
            exists_affix, affix_info = self.affix_manager.get_affix_definition(part)
            if exists_affix:
                result += f"✓ '{part}' - 已存在: {affix_info}\n"
            else:
                result += f"✗ '{part}' - 可添加为新词缀\n"
        
        result += "\n💬 建议: 使用\"添加词缀\"标签添加这些词缀及其释义"
        
        return result
    
    def make_css_html(self) -> str:
        """生成 CSS HTML 字符串用于页面立即注入（使用字体倍率，保持相对大小）"""
        en = getattr(self, 'en_font', 'Arial')
        zh = getattr(self, 'zh_font', 'SimHei')
        # 倍率范围 80%-150%，转换为倍数（100% = 1.0）
        scale = getattr(self, 'font_size', 100) / 100.0
        style = getattr(self, 'font_style', 'normal')
        weight = '400'
        font_style = 'normal'
        
        if style == 'italic':
            font_style = 'italic'
        elif style == 'bold':
            weight = '700'
        elif style == 'bold-italic':
            weight = '700'
            font_style = 'italic'
        
        # 清理字体名称（移除可能的无效字符或多个字体声明）
        en_clean = en.split(',')[0].strip() if ',' in en else en
        zh_clean = zh.split(',')[0].strip() if ',' in zh else zh
        
        # 生成覆盖力强的 CSS，使用倍率而非固定大小（保留 MD 标题相对大小）
        css = f"""
<style>
:root {{
  --lex-font-scale: {scale};
  --lex-font-weight: {weight};
  --lex-font-style: {font_style};
}}

/* 基础字体设置（不覆盖标题） */
body, div, span, p, label, button, input, textarea, select {{
  font-family: '{en_clean}', '{zh_clean}', Arial, Helvetica, sans-serif !important;
  font-size: calc(1em * var(--lex-font-scale)) !important;
  font-weight: var(--lex-font-weight) !important;
  font-style: var(--lex-font-style) !important;
}}

/* 针对 Gradio 容器（不覆盖标题） */
.gradio-container {{
  font-size-adjust: none;
}}

.gradio-container > div:not(h1):not(h2):not(h3):not(h4):not(h5):not(h6),
.gradio-container span,
.gradio-container p,
.gradio-container label,
.gradio-container button {{
  font-family: '{en_clean}', '{zh_clean}', Arial, sans-serif !important;
  font-size: calc(1em * var(--lex-font-scale)) !important;
  font-weight: var(--lex-font-weight) !important;
  font-style: var(--lex-font-style) !important;
}}

/* 文本输入框 */
input[type="text"],
input[type="password"],
input[type="email"],
textarea,
.gradio-textbox input,
.gradio-textbox textarea {{
  font-family: '{en_clean}', '{zh_clean}', monospace !important;
  font-size: calc(1em * var(--lex-font-scale)) !important;
  font-weight: var(--lex-font-weight) !important;
}}

/* 按钮文本 */
button, .gr-button {{
  font-family: '{en_clean}', '{zh_clean}', Arial, sans-serif !important;
  font-size: calc(1em * var(--lex-font-scale)) !important;
  font-weight: var(--lex-font-weight) !important;
}}

/* 保留 Markdown 标题的相对大小 */
.gradio-markdown h1 {{
  font-size: calc(2em * var(--lex-font-scale)) !important;
  font-family: '{en_clean}', '{zh_clean}', Arial, sans-serif !important;
}}

.gradio-markdown h2 {{
  font-size: calc(1.5em * var(--lex-font-scale)) !important;
  font-family: '{en_clean}', '{zh_clean}', Arial, sans-serif !important;
}}

.gradio-markdown h3 {{
  font-size: calc(1.25em * var(--lex-font-scale)) !important;
  font-family: '{en_clean}', '{zh_clean}', Arial, sans-serif !important;
}}

.gradio-markdown p {{
  font-family: '{en_clean}', '{zh_clean}', Arial, sans-serif !important;
  font-size: calc(1em * var(--lex-font-scale)) !important;
}}
</style>
"""
        return css

    def make_theme(self):
        """根据当前设置返回 Gradio 主题实例"""
        try:
            theme_instance = self.theme_instances.get(self.theme, None)
            if theme_instance is not None:
                return theme_instance
            else:
                return gr.themes.Soft()
        except Exception:
            return gr.themes.Default()
    
    def _auto_save(self):
        """自动保存"""
        self.manager.save(self.default_save_path)
    
    def build_interface(self) -> gr.Blocks:
        """构建Gradio界面"""
        
        # 选择主题类（Gradio 要求 theme 为 class），并在 Blocks 中传递该类
        theme_obj = self.make_theme()
        with gr.Blocks(title="LextrieBloom - 单词积累本", theme=theme_obj) as demo:
            gr.Markdown(f"""
            # LextrieBloom
            ## 高效的单词积累本
            
            基于Trie数据结构的高效单词管理工具。支持导入、查询、统计等功能。
            """)
            # 在构建界面时注入初始化 CSS，以应用启动时的字体/样式设置
            css_output = gr.HTML(self.make_css_html())
            
            with gr.Tabs():
                # 页签1: 添加单词
                with gr.TabItem("➕ 添加单词"):
                    with gr.Row():
                        word_input = gr.Textbox(
                            label="单词",
                            placeholder="输入要添加的单词",
                            max_lines=1
                        )
                        definition_input = gr.Textbox(
                            label="释义",
                            placeholder="输入单词释义（可选）",
                            lines=2
                        )
                    
                    add_btn = gr.Button("➕ 添加", variant="primary")
                    add_output = gr.Textbox(label="结果", interactive=False)
                    
                    add_btn.click(
                        fn=self.add_single_word,
                        inputs=[word_input, definition_input],
                        outputs=add_output
                    )
                
                # 页签2: 导入文件
                with gr.TabItem("📤 导入文件"):
                    gr.Markdown("上传单词文件（格式：每行一个 `单词 释义`，或直接单词）")
                    
                    file_input = gr.File(
                        label="选择文件",
                        file_types=[".txt"]
                    )
                    import_btn = gr.Button("📤 导入", variant="primary")
                    import_output = gr.Textbox(label="导入结果", interactive=False)
                    
                    import_btn.click(
                        fn=self.import_file,
                        inputs=file_input,
                        outputs=import_output
                    )
                
                # 页签3: 查询单词
                with gr.TabItem("🔍 精确查询"):
                    search_input = gr.Textbox(
                        label="输入单词",
                        placeholder="输入要查询的单词",
                        max_lines=1
                    )
                    search_btn = gr.Button("🔍 查询", variant="primary")
                    search_output = gr.Textbox(label="查询结果", interactive=False, lines=3)
                    
                    search_btn.click(
                        fn=self.search_word_ui,
                        inputs=search_input,
                        outputs=search_output
                    )
                
                # 页签4: 前缀查询
                with gr.TabItem("🔎 前缀查询"):
                    prefix_input = gr.Textbox(
                        label="输入前缀",
                        placeholder="输入前缀以查询相关单词",
                        max_lines=1
                    )
                    prefix_btn = gr.Button("🔎 查询", variant="primary")
                    prefix_output = gr.Textbox(
                        label="查询结果",
                        interactive=False,
                        lines=10
                    )
                    
                    prefix_btn.click(
                        fn=self.prefix_search_ui,
                        inputs=prefix_input,
                        outputs=prefix_output
                    )
                
                # 页签5: 列出所有
                with gr.TabItem("📋 查看所有"):
                    list_btn = gr.Button("📋 刷新列表", variant="primary")
                    list_output = gr.Textbox(
                        label="所有单词",
                        interactive=False,
                        lines=15
                    )
                    
                    list_btn.click(
                        fn=self.list_all_ui,
                        inputs=[],
                        outputs=list_output
                    )
                
                # 页签6: 删除单词
                with gr.TabItem("🗑️ 删除单词"):
                    delete_input = gr.Textbox(
                        label="输入单词",
                        placeholder="输入要删除的单词",
                        max_lines=1
                    )
                    delete_btn = gr.Button("🗑️ 删除", variant="stop")
                    delete_output = gr.Textbox(label="删除结果", interactive=False)
                    
                    delete_btn.click(
                        fn=self.delete_word_ui,
                        inputs=delete_input,
                        outputs=delete_output
                    )
                
                # 页签7: 数据管理
                with gr.TabItem("💾 数据管理"):
                    with gr.Group():
                        gr.Markdown("### 📊 统计信息")
                        stats_btn = gr.Button("📊 刷新统计", variant="primary")
                        stats_output = gr.Textbox(
                            label="统计结果",
                            interactive=False,
                            lines=3
                        )
                        
                        stats_btn.click(
                            fn=self.get_stats_ui,
                            inputs=[],
                            outputs=stats_output
                        )
                    
                    with gr.Group():
                        gr.Markdown("### 💾 保存/加载")
                        with gr.Row():
                            save_path = gr.Textbox(
                                label="保存路径",
                                placeholder="例: vocabulary.json",
                                value=self.default_save_path
                            )
                            save_btn = gr.Button("💾 保存", variant="primary")
                        save_output = gr.Textbox(label="保存结果", interactive=False)
                        
                        save_btn.click(
                            fn=self.save_to_file_ui,
                            inputs=save_path,
                            outputs=save_output
                        )
                        
                        with gr.Row():
                            load_path = gr.Textbox(
                                label="加载路径",
                                placeholder="例: vocabulary.json",
                                value=self.default_save_path
                            )
                            load_btn = gr.Button("📂 加载", variant="primary")
                        load_output = gr.Textbox(label="加载结果", interactive=False)
                        
                        load_btn.click(
                            fn=self.load_from_file_ui,
                            inputs=load_path,
                            outputs=load_output
                        )
                    
                    with gr.Group():
                        gr.Markdown("### 📤 导出数据")
                        with gr.Row():
                            export_path = gr.Textbox(
                                label="导出路径",
                                placeholder="例: vocabulary_export.txt"
                            )
                            export_format = gr.Dropdown(
                                choices=["txt", "json", "csv"],
                                label="导出格式",
                                value="txt"
                            )
                        
                        export_btn = gr.Button("📤 导出", variant="primary")
                        export_output = gr.Textbox(label="导出结果", interactive=False)
                        
                        export_btn.click(
                            fn=self.export_file_ui,
                            inputs=[export_path, export_format],
                            outputs=export_output
                        )
                    
                    with gr.Group():
                        gr.Markdown("### 🔧 高级选项")
                        # 删除所有数据
                        gr.Markdown("**⚠️ 警告区域**")
                        delete_all_btn = gr.Button("🗑️ 清除所有数据", variant="stop")
                        delete_all_output = gr.Textbox(label="清除结果", interactive=False)
                        
                        delete_all_btn.click(
                            fn=self.delete_all_data_ui,
                            inputs=[],
                            outputs=delete_all_output
                        )
                
                # 页签8: 词缀管理
                with gr.TabItem("🔤 词缀管理"):
                    with gr.Group():
                        gr.Markdown("### ➕ 添加词缀")
                        with gr.Row():
                            affix_input = gr.Textbox(
                                label="词缀",
                                placeholder="例: un-, -tion, -ly",
                                max_lines=1
                            )
                            affix_definition = gr.Textbox(
                                label="释义",
                                placeholder="词缀的含义",
                                lines=2
                            )
                            affix_category = gr.Dropdown(
                                choices=["前缀", "后缀", "中缀", "其他"],
                                value="后缀",
                                label="分类"
                            )
                        
                        add_affix_btn = gr.Button("➕ 添加词缀", variant="primary")
                        add_affix_output = gr.Textbox(label="结果", interactive=False)
                        
                        add_affix_btn.click(
                            fn=self.add_affix_ui,
                            inputs=[affix_input, affix_definition, affix_category],
                            outputs=add_affix_output
                        )
                    
                    with gr.Group():
                        gr.Markdown("### 🔍 查询词缀释义")
                        query_affix_input = gr.Textbox(
                            label="词缀",
                            placeholder="输入要查询的词缀",
                            max_lines=1
                        )
                        query_affix_btn = gr.Button("🔍 查询", variant="primary")
                        query_affix_output = gr.Textbox(label="查询结果", interactive=False, lines=3)
                        
                        query_affix_btn.click(
                            fn=self.query_affix_definition_ui,
                            inputs=query_affix_input,
                            outputs=query_affix_output
                        )
                    
                    with gr.Group():
                        gr.Markdown("### 📋 查看所有词缀")
                        list_affix_btn = gr.Button("📋 刷新列表", variant="primary")
                        list_affix_output = gr.Textbox(label="词缀列表", interactive=False, lines=15)
                        
                        list_affix_btn.click(
                            fn=self.list_all_affixes_ui,
                            inputs=[],
                            outputs=list_affix_output
                        )
                
                # 页签9: 词缀分类与分析
                with gr.TabItem("📚 词缀分析"):
                    with gr.Group():
                        gr.Markdown("### 📊 按词缀分类单词")
                        categorize_btn = gr.Button("📊 分析分类", variant="primary")
                        categorize_output = gr.Textbox(label="分类结果", interactive=False, lines=20)
                        
                        categorize_btn.click(
                            fn=self.categorize_words_by_affix_ui,
                            inputs=[],
                            outputs=categorize_output
                        )
                    
                    with gr.Group():
                        gr.Markdown("### 🔍 检测潜在词缀")
                        detect_btn = gr.Button("🔍 检测", variant="primary")
                        detect_output = gr.Textbox(label="检测结果", interactive=False, lines=10)
                        
                        detect_btn.click(
                            fn=self.detect_affixes_ui,
                            inputs=[],
                            outputs=detect_output
                        )
                
                # 页签10: 统计分析
                with gr.TabItem("📊 统计分析"):
                    with gr.Group():
                        gr.Markdown("### 📈 每日加入热力图")
                        daily_btn = gr.Button("📈 生成热力图", variant="primary")
                        daily_output = gr.Textbox(label="热力图", interactive=False, lines=20)
                        
                        daily_btn.click(
                            fn=self.get_daily_statistics_ui,
                            inputs=[],
                            outputs=daily_output
                        )
                    
                    with gr.Group():
                        gr.Markdown("### ⏰ 单词加入时间记录")
                        timestamp_btn = gr.Button("⏰ 查看时间记录", variant="primary")
                        timestamp_output = gr.Textbox(label="时间记录", interactive=False, lines=15)
                        
                        timestamp_btn.click(
                            fn=self.get_word_timestamps_ui,
                            inputs=[],
                            outputs=timestamp_output
                        )
                    
                    with gr.Group():
                        gr.Markdown("### 📈 最近N天的新增单词")
                        trending_days = gr.Number(
                            value=7,
                            label="天数",
                            info="显示最近多少天的单词"
                        )
                        trending_btn = gr.Button("📈 查看趋势", variant="primary")
                        trending_output = gr.Textbox(label="趋势", interactive=False, lines=15)
                        
                        trending_btn.click(
                            fn=self.get_trending_words_ui,
                            inputs=trending_days,
                            outputs=trending_output
                        )
                    
                    with gr.Group():
                        gr.Markdown("### 📅 时间范围查询")
                        with gr.Row():
                            start_date = gr.Textbox(
                                label="开始日期",
                                placeholder="YYYY-MM-DD",
                                max_lines=1
                            )
                            end_date = gr.Textbox(
                                label="结束日期",
                                placeholder="YYYY-MM-DD",
                                max_lines=1
                            )
                        
                        range_btn = gr.Button("📅 查询范围", variant="primary")
                        range_output = gr.Textbox(label="范围查询结果", interactive=False, lines=10)
                        
                        range_btn.click(
                            fn=self.query_time_range_ui,
                            inputs=[start_date, end_date],
                            outputs=range_output
                        )
                
                # 页签11: Fail跳转建议
                with gr.TabItem("💡 查询帮助"):
                    with gr.Group():
                        gr.Markdown("### ❓ 单词不存在时的建议")
                        gr.Markdown("如果查询的单词不在词库中，系统会建议您将相关部分存入词缀库")
                        
                        fail_word_input = gr.Textbox(
                            label="输入单词",
                            placeholder="输入不在词库中的单词",
                            max_lines=1
                        )
                        fail_btn = gr.Button("❓ 获取建议", variant="primary")
                        fail_output = gr.Textbox(label="建议", interactive=False, lines=8)
                        
                        fail_btn.click(
                            fn=self.fail_jump_affix_suggestion_ui,
                            inputs=fail_word_input,
                            outputs=fail_output
                        )
                
                # 页签12: 设置
                with gr.TabItem("⚙️ 设置"):
                    with gr.Group():
                        gr.Markdown("### 🔤 字体设置")
                        
                        # 英文字体
                        en_font_input = gr.Textbox(
                            label="英文字体名称",
                            value=self.en_font,
                            placeholder="例: Arial, Times New Roman, Courier"
                        )
                        
                        # 中文字体
                        zh_font_input = gr.Textbox(
                            label="中文字体名称",
                            value=self.zh_font,
                            placeholder="例: SimHei, SimSun, Microsoft YaHei"
                        )
                        
                        font_apply_btn = gr.Button("💾 应用字体", variant="primary")
                        font_result = gr.Textbox(label="设置结果", interactive=False)
                        font_css = gr.HTML()  # 隐藏输出用于接收 CSS
                        
                        font_apply_btn.click(
                            fn=self.set_fonts,
                            inputs=[en_font_input, zh_font_input],
                            outputs=[font_result, font_css]
                        )
                    
                    with gr.Group():
                        gr.Markdown("### 📏 字体倍率")
                        
                        font_size_slider = gr.Slider(
                            minimum=95,
                            maximum=120,
                            value=self.font_size,
                            step=0.001,
                            label="字体倍率 (%)",
                            info="90%-120%（影响文本及输入框，保持标题相对大小）"
                        )
                        
                        size_apply_btn = gr.Button("💾 应用倍率", variant="primary")
                        size_result = gr.Textbox(label="设置结果", interactive=False)
                        size_css = gr.HTML()  # 隐藏输出用于接收 CSS
                        
                        size_apply_btn.click(
                            fn=self.set_font_size,
                            inputs=font_size_slider,
                            outputs=[size_result, size_css]
                        )
                    
                    with gr.Group():
                        gr.Markdown("### 🎨 字体样式")
                        
                        font_style_dropdown = gr.Dropdown(
                            choices=["normal", "italic", "bold", "bold-italic"],
                            value=self.font_style,
                            label="字体样式",
                            info="正常 / 斜体 / 加粗 / 加粗斜体"
                        )
                        
                        style_apply_btn = gr.Button("💾 应用样式", variant="primary")
                        style_result = gr.Textbox(label="设置结果", interactive=False)
                        style_css = gr.HTML()  # 隐藏输出用于接收 CSS
                        
                        style_apply_btn.click(
                            fn=self.set_font_style,
                            inputs=font_style_dropdown,
                            outputs=[style_result, style_css]
                        )
                    
                    with gr.Group():
                        gr.Markdown("### 🌈 颜色主题")
                        
                        # 扩展主题列表，并用中文标签显示
                        theme_choices = list(self.themes_dict.keys())
                        theme_labels_list = [self.theme_labels.get(t, t) for t in theme_choices]
                        
                        theme_dropdown = gr.Dropdown(
                            choices=theme_choices,
                            value=self.theme,
                            label="选择主题",
                            info="选择 Gradio 内置主题"
                        )
                        
                        # 在 Dropdown 旁边显示标签（可选：也可通过 label 映射）
                        gr.Markdown(
                            "**可用主题：** " + " | ".join(
                                [f"{label} ({key})" for key, label in self.theme_labels.items()]
                            )
                        )
                        
                        theme_apply_btn = gr.Button("🔄 应用主题（将自动刷新）", variant="primary")
                        theme_result = gr.Textbox(label="设置结果", interactive=False)
                        theme_refresh = gr.HTML()  # 隐藏输出用于接收刷新脚本
                        
                        theme_apply_btn.click(
                            fn=self.set_theme,
                            inputs=theme_dropdown,
                            outputs=[theme_result, theme_refresh]
                        )
                
                # 页签13: 帮助
                with gr.TabItem("❓ 帮助"):
                    gr.Markdown("""
                    ## LextrieBloom 使用说明
                    
                    ### ➕ 添加单词
                    - 输入单词和释义，点击添加按钮
                    - 释义为可选项
                    
                    ### 📤 导入文件
                    - 上传txt文件，每行格式: `单词 释义`
                    - 支持注释行（以#开头）
                    - 自动处理空行
                    
                    ### 🔍 精确查询
                    - 查询完整的单词及其释义
                    
                    ### 🔎 前缀查询
                    - 查询所有以某个前缀开头的单词
                    - 结果按字典序排序
                    
                    ### 📋 查看所有
                    - 列出所有已添加的单词
                    - 按字典序排序
                    
                    ### 🗑️ 删除单词
                    - 删除指定的单词
                    
                    ### 💾 数据管理
                    - **保存**: 将当前单词本保存到JSON/Pickle文件
                    - **加载**: 从保存的文件中加载单词本
                    - **导出**: 导出为TXT/JSON/CSV格式
                    - **清除所有数据**: 清空整个词库并删除保存文件（谨慎使用！）
                    
                    ### ⚙️ 设置
                    - **字体**: 自定义英文和中文字体名称（修改后点击"应用字体"立即生效，无需刷新）
                    - **字体倍率**: 用滑块调整显示倍率（80%-150%，修改后点击"应用倍率"立即生效，标题大小会自动缩放）
                    - **字体样式**: 选择正常、斜体、加粗或加粗斜体（修改后点击"应用样式"立即生效）
                    - **颜色主题**: 从 7 个 Gradio 内置主题中选择（点击"应用主题"会自动刷新页面以生效）
                    
                    ### 🔤 词缀管理
                    - **添加词缀**: 添加新的词缀（前缀/后缀）及其释义
                    - **查询词缀**: 查询特定词缀的释义
                    - **查看所有**: 列出所有已添加的词缀，按分类显示
                    
                    ### 📚 词缀分析
                    - **按词缀分类**: 将词库中的单词按词缀自动分类
                    - **检测潜在词缀**: 从已有单词中检测高频词缀，帮助构建词缀库
                    
                    ### 📊 统计分析
                    - **每日热力图**: 显示每天加入多少个单词的统计图表
                    - **加入时间记录**: 查看每个单词的加入时间（最新的单词优先显示）
                    - **趋势分析**: 查看最近N天新增的单词
                    - **时间范围查询**: 按日期范围查询单词加入记录
                    
                    ### 💡 查询帮助
                    - **Fail跳转建议**: 当查询的单词不在词库中时，系统自动建议相关词缀供添加
                    - 帮助用户快速积累和组织词缀库
                    
                    ## 文件格式示例
                    
                    ```
                    # 这是注释
                    apple 苹果
                    book 书籍
                    cat 猫
                    ```
                    
                    ## 特性
                    
                    - ⚡ 基于Trie数据结构，高效查询
                    - 💾 支持多种存储格式（JSON、Pickle、CSV）
                    - 🔍 支持精确查询和前缀查询
                    - 📤 支持文件导入导出
                    - ⏰ 单词加入时间记录和统计分析
                    - 🔤 词缀管理和自动分类
                    - 📊 每日热力图统计
                    - 💡 Fail跳转智能建议
                    - 🎯 自动保存功能
                    - 🎨 字体/样式/主题自定义（设置持久化到 settings.json）
                    - 🔧 易于扩展的架构
                    
                    copyright © 2025 [FlowerAccepted](luogu.com.cn/user/1023732)
                    """)
        
        return demo


def launch_app():
    """启动应用"""
    ui = VocabularyUI()
    demo = ui.build_interface()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    launch_app()
