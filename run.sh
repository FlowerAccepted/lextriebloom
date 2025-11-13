#!/bin/bash
# 单词积累本快速启动脚本

echo "🚀 单词积累本启动脚本"
echo "========================"

# 检查Python版本
python_version=$(python3 --version 2>&1)
echo "📦 Python版本: $python_version"

# 检查是否已安装依赖
echo ""
echo "📥 检查依赖..."

if ! python3 -c "import gradio" 2>/dev/null; then
    echo "❌ 未检测到gradio，正在安装依赖..."
    pip install -r requirements.txt
else
    echo "✅ 依赖已安装"
fi

# 运行应用
echo ""
echo "🎯 启动应用..."
echo "📱 请在浏览器中打开: http://127.0.0.1:7860"
echo ""

python3 main.py
