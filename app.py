# 导入并启动邮件MCP服务器
from email_mcp_server import demo

if __name__ == "__main__":
    # 启动Gradio应用，并启用MCP服务器
    demo.launch(mcp_server=True)
