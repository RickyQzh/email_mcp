#!/bin/bash

# 检查是否安装了mcp-remote
if ! command -v npx &> /dev/null; then
    echo "请先安装Node.js和npm"
    exit 1
fi

# 使用mcp-remote连接到Gradio MCP服务器
echo "正在连接到Gradio MCP服务器..."
npx mcp-remote http://localhost:7860/gradio_api/mcp/sse

# 如果连接中断，显示错误信息
echo "MCP客户端连接已断开"