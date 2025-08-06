import requests
import json
import time

def test_mcp_connection():
    """测试MCP服务器连接和Schema"""
    try:
        # 获取MCP服务器的Schema
        schema_url = "http://localhost:7860/gradio_api/mcp/schema"
        response = requests.get(schema_url)
        
        if response.status_code == 200:
            schema = response.json()
            print("MCP服务器连接成功！")
            print("\n可用工具列表：")
            
            # 打印可用的工具
            for tool in schema.get("tools", []):
                print(f"- {tool.get('name')}: {tool.get('description')}")
                print(f"  参数: {json.dumps(tool.get('parameters'), ensure_ascii=False, indent=2)}")
                print()
                
            return True
        else:
            print(f"连接失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"连接测试出错: {e}")
        return False

if __name__ == "__main__":
    print("正在测试MCP服务器连接...")
    
    # 等待几秒钟，确保服务器已启动
    time.sleep(2)
    
    test_mcp_connection()