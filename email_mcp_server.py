import os
import gradio as gr
from typing import Optional, List, Dict, Any, Union

# 导入环境变量配置
from email_config import IMAP_SERVER, SMTP_SERVER, ACCOUNT, PASSWORD

# 导入163邮箱接收模块
from receive_163 import Email
# 导入163邮箱发送模块
from send_163 import EmailSender

def get_newest_email() -> Dict[str, Any]:
    """
    获取最新的未读邮件，包括发件人、主题、内容和附件信息。
    
    Returns:
        Dict: 包含邮件信息的字典，包括发件人、主题、日期、内容和附件列表
    """
    email_163 = Email(imap=IMAP_SERVER, account=ACCOUNT, password=PASSWORD)
    msg_data = email_163.get_newest()
    return {
        "from": msg_data.get('from', '未知'),
        "subject": msg_data.get('subject', '无主题'),
        "date": msg_data.get('date', '未知'),
        "content": msg_data.get('content', ''),
        "files": msg_data.get('files', [])
    }

def check_emails(message_type: str = "Unseen", count: int = 5) -> List[Dict[str, Any]]:
    """
    检查指定类型和数量的邮件。
    
    Args:
        message_type (str): 邮件类型，可选值包括 "All", "Unseen", "Seen", "Recent", "Answered", "Flagged"
        count (int): 要检索的邮件数量
        
    Returns:
        List[Dict]: 包含邮件信息的字典列表
    """
    email_163 = Email(imap=IMAP_SERVER, account=ACCOUNT, password=PASSWORD)
    messages = []
    
    # 设置为False以获取多封邮件，而不仅仅是最新的一封
    for msg_data in email_163.check_email(last_message=False, message_type=message_type, count=count):
        messages.append({
            "from": msg_data.get('from', '未知'),
            "subject": msg_data.get('subject', '无主题'),
            "date": msg_data.get('date', '未知'),
            "content": msg_data.get('content', ''),
            "files": msg_data.get('files', [])
        })
    
    return messages

def save_attachment(file_name: str, save_path: str = '') -> str:
    """
    保存指定的附件到指定路径。
    
    Args:
        file_name (str): 要保存的附件文件名
        save_path (str): 保存路径，默认为空（当前目录）
        
    Returns:
        str: 保存的文件路径
    """
    email_163 = Email(imap=IMAP_SERVER, account=ACCOUNT, password=PASSWORD, file_save_path=save_path)
    msg_data = email_163.get_newest()
    
    # 检查附件是否存在
    files = msg_data.get('files', [])
    if file_name in files:
        # 文件已经在获取邮件时被保存
        file_path = os.path.join(save_path, file_name)
        if os.path.exists(file_path):
            return f"文件已保存到 {file_path}"
        else:
            return f"文件保存失败"
    else:
        return f"未找到名为 {file_name} 的附件"

def send_text_email(to_addr: Union[str, List[str]], subject: str, content: str, cc_addr: Union[str, List[str], None] = None) -> Dict[str, str]:
    """
    发送纯文本邮件
    
    Args:
        to_addr (str or list): 收件人邮箱地址，可以是单个字符串或字符串列表
        subject (str): 邮件主题
        content (str): 邮件正文内容
        cc_addr (str or list, optional): 抄送人邮箱地址，可以是单个字符串或字符串列表
        
    Returns:
        dict: 包含发送状态和消息的字典
    """
    sender = EmailSender()
    return sender.send_text_email(to_addr, subject, content, cc_addr)

def send_html_email(to_addr: Union[str, List[str]], subject: str, html_content: str, cc_addr: Union[str, List[str], None] = None) -> Dict[str, str]:
    """
    发送HTML格式邮件
    
    Args:
        to_addr (str or list): 收件人邮箱地址，可以是单个字符串或字符串列表
        subject (str): 邮件主题
        html_content (str): HTML格式的邮件正文内容
        cc_addr (str or list, optional): 抄送人邮箱地址，可以是单个字符串或字符串列表
        
    Returns:
        dict: 包含发送状态和消息的字典
    """
    sender = EmailSender()
    return sender.send_html_email(to_addr, subject, html_content, cc_addr)

def send_email_with_attachment(to_addr: Union[str, List[str]], subject: str, content: str, 
                              attachment_paths: Union[str, List[str]], cc_addr: Union[str, List[str], None] = None, 
                              is_html: bool = False) -> Dict[str, str]:
    """
    发送带附件的邮件
    
    Args:
        to_addr (str or list): 收件人邮箱地址，可以是单个字符串或字符串列表
        subject (str): 邮件主题
        content (str): 邮件正文内容
        attachment_paths (str or list): 附件路径，可以是单个字符串或字符串列表
        cc_addr (str or list, optional): 抄送人邮箱地址，可以是单个字符串或字符串列表
        is_html (bool, optional): 内容是否为HTML格式，默认为False
        
    Returns:
        dict: 包含发送状态和消息的字典
    """
    sender = EmailSender()
    return sender.send_email_with_attachment(to_addr, subject, content, attachment_paths, cc_addr, is_html)

# 创建Gradio界面
with gr.Blocks(title="163邮箱MCP服务器") as demo:
    gr.Markdown("# 163邮箱MCP服务器")
    gr.Markdown("这是一个基于Gradio的163邮箱MCP服务器，可以获取最新邮件、检查邮件列表和保存附件。")
    
    # 添加API端点，这些将作为MCP工具暴露给LLM
    gr.api(get_newest_email)
    gr.api(check_emails)
    gr.api(save_attachment)
    gr.api(send_text_email)
    gr.api(send_html_email)
    gr.api(send_email_with_attachment)

if __name__ == "__main__":
    # 启动Gradio应用，并启用MCP服务器
    demo.launch(mcp_server=True)