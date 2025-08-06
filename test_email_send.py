import requests
import json
import time

def test_send_email():
    """测试发送邮件功能"""
    # MCP服务器地址
    mcp_url = "http://localhost:7860/gradio_api/mcp/sse"
    
    # 测试收件人邮箱（请替换为实际的测试邮箱）
    test_email = "test@example.com"
    
    # 测试发送纯文本邮件
    print("\n1. 测试发送纯文本邮件...")
    try:
        # 构建API请求数据
        data = {
            "to_addr": test_email,
            "subject": "MCP服务器测试邮件",
            "content": "这是一封来自MCP服务器的测试邮件。\n\n如果您收到此邮件，说明MCP服务器的发送功能正常工作。"
        }
        
        # 发送请求
        response = requests.post(
            "http://localhost:7860/gradio_api/mcp/run/send_text_email",
            json=data
        )
        
        # 检查响应
        if response.status_code == 200:
            result = response.json()
            print(f"发送结果: {json.dumps(result, ensure_ascii=False)}")
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"发送纯文本邮件测试出错: {e}")
    
    # 测试发送HTML邮件
    print("\n2. 测试发送HTML邮件...")
    try:
        # 构建API请求数据
        data = {
            "to_addr": test_email,
            "subject": "MCP服务器HTML测试邮件",
            "html_content": """
            <html>
            <body>
                <h1>HTML测试邮件</h1>
                <p>这是一封来自MCP服务器的<strong>HTML格式</strong>测试邮件。</p>
                <p>如果您收到此邮件，说明MCP服务器的HTML邮件发送功能正常工作。</p>
            </body>
            </html>
            """
        }
        
        # 发送请求
        response = requests.post(
            "http://localhost:7860/gradio_api/mcp/run/send_html_email",
            json=data
        )
        
        # 检查响应
        if response.status_code == 200:
            result = response.json()
            print(f"发送结果: {json.dumps(result, ensure_ascii=False)}")
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"发送HTML邮件测试出错: {e}")
    
    print("\n测试完成！")

if __name__ == "__main__":
    print("正在测试MCP服务器的邮件发送功能...")
    
    # 等待几秒钟，确保服务器已启动
    time.sleep(2)
    
    test_send_email()