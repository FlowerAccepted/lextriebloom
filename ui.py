"""
使用Gradio构建的交互式用户界面
"""

import gradio as gr
from vocabulary_manager import VocabularyManager, JSONStorage, PickleStorage
from pathlib import Path


class VocabularyUI:
    """单词积累本的Gradio用户界面"""
    
    def __init__(self):
        self.manager = VocabularyManager(storage_backend=JSONStorage())
        self.default_save_path = "vocabulary.json"
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
        _, result = self.manager.search_word(word)
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
    
    def _auto_save(self):
        """自动保存"""
        self.manager.save(self.default_save_path)
    
    def build_interface(self) -> gr.Blocks:
        """构建Gradio界面"""
        
        with gr.Blocks(title="📚 单词积累本", theme=gr.themes.Soft()) as demo:
            gr.Markdown("""
            # 📚 单词积累本
            
            基于Trie数据结构的高效单词管理工具。支持导入、查询、统计等功能。
            """)
            
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
                
                # 页签8: 帮助
                with gr.TabItem("❓ 帮助"):
                    gr.Markdown("""
                    ## 使用说明
                    
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
                    - 🎯 自动保存功能
                    - 🔧 易于扩展的架构
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
