---
# 详细文档见https://modelscope.cn/docs/%E5%88%9B%E7%A9%BA%E9%97%B4%E5%8D%A1%E7%89%87
domain: #领域：cv/nlp/audio/multi-modal/AutoML
# - cv
tags: #自定义标签
-
datasets: #关联数据集
  evaluation:
  #- iic/ICDAR13_HCTR_Dataset
  test:
  #- iic/MTWI
  train:
  #- iic/SIBR
models: #关联模型
#- iic/ofa_ocr-recognition_general_base_zh

## 启动文件(若SDK为Gradio/Streamlit，默认为app.py, 若为Static HTML, 默认为index.html)
deployspec:
  entry_file: email_mcp_server.py
license: Apache License 2.0
---

# 163邮箱 MCP 服务器

这是一个基于Gradio的163邮箱MCP服务器，可以作为LLM的工具，用于获取和处理电子邮件。

## 功能

- 获取最新的未读邮件
- 检查指定类型和数量的邮件
- 保存邮件附件
- 发送纯文本邮件
- 发送HTML格式邮件
- 发送带附件的邮件

## 安装依赖

### 使用requirements.txt安装

```bash
pip install -r requirements.txt
```

### 手动安装

```bash
pip install gradio[mcp] bs4 python-dotenv
```

## 启动服务器

### 直接启动

```bash
python email_mcp_server.py
```

### 使用环境变量启动

可以通过环境变量来配置邮箱账号信息：

```bash
chmod +x start_with_env.sh
./start_with_env.sh
```

或者手动设置环境变量：

```bash
export EMAIL_IMAP_SERVER=imap.163.com
export EMAIL_SMTP_SERVER=smtp.163.com
export EMAIL_ACCOUNT=your_email@163.com
export EMAIL_PASSWORD=your_password
python email_mcp_server.py
```


## MCP工具

服务器提供以下MCP工具：

1. `get_newest_email` - 获取最新的未读邮件
2. `check_emails` - 检查指定类型和数量的邮件
3. `save_attachment` - 保存指定的附件
4. `send_text_email` - 发送纯文本邮件
5. `send_html_email` - 发送HTML格式邮件
6. `send_email_with_attachment` - 发送带附件的邮件

## 连接到MCP客户端

MCP服务器启动后，可以通过以下URL连接：

```
http://localhost:7860/gradio_api/mcp/sse
```

#### Clone with HTTP
```bash
 git clone https://www.modelscope.cn/studios/s3219521aa/email_mcp.git
```