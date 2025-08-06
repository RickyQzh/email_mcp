#!/bin/bash

# 确保脚本在后台运行
nohup python email_mcp_server.py > email_mcp_server.log 2>&1 &

# 打印进程ID，方便后续管理
echo "Email MCP服务器已在后台启动，进程ID: $!"
echo "日志文件: email_mcp_server.log"