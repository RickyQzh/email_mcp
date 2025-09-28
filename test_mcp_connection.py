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
            data = response.json()
            print("MCP服务器连接成功！")

            # 兼容返回结构：可能是 {"tools": [...]} 或直接是 [...]
            tools = []
            if isinstance(data, dict):
                tools = data.get("tools") or []
            elif isinstance(data, list):
                tools = data

            print("\n可用工具列表：")
            if not tools:
                # 如果没有解析到工具，打印原始响应以便排查
                print("(未在schema中发现工具列表，原始响应如下)")
                try:
                    print(json.dumps(data, ensure_ascii=False, indent=2))
                except Exception:
                    print(str(data))
                return True

            for tool in tools:
                if isinstance(tool, dict):
                    name = tool.get("name") or tool.get("id") or "(unknown)"
                    desc = tool.get("description") or ""
                    params = tool.get("parameters")
                    print(f"- {name}: {desc}")
                    if params is not None:
                        print(f"  参数: {json.dumps(params, ensure_ascii=False, indent=2)}")
                else:
                    # 工具条目不是字典时，直接打印
                    print(f"- {tool}")
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