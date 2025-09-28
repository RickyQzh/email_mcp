import os
import gradio as gr
from typing import Optional, List, Dict, Any, Union

# 服务器自动匹配工具
from email_config import get_imap_server, get_smtp_server

# 导入163邮箱接收模块
from receive_163 import Email
# 导入163邮箱发送模块
from send_163 import EmailSender

def get_newest_email(
    account: str,
    password: str,
    imap_server: Optional[str] = None,
) -> Dict[str, Any]:
    """
    获取最新的未读邮件，包括发件人、主题、内容和附件信息。
    
    Returns:
        Dict: 包含邮件信息的字典，包括发件人、主题、日期、内容和附件列表

    必填参数:
        account (str): 邮箱账号
        password (str): 授权码/密码

    可选参数:
        imap_server (str, optional): 自定义IMAP服务器地址；未提供时自动匹配
    """
    if not account or not password:
        raise ValueError("account 和 password 为必填参数")
    email_163 = Email(
        imap=imap_server or get_imap_server(account),
        account=account,
        password=password,
    )
    msg_data = email_163.get_newest()
    return {
        "from": msg_data.get('from', '未知'),
        "subject": msg_data.get('subject', '无主题'),
        "date": msg_data.get('date', '未知'),
        "content": msg_data.get('content', ''),
        "files": msg_data.get('files', [])
    }

def check_emails(
    account: str,
    password: str,
    message_type: str = "Unseen",
    count: int = 5,
    imap_server: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    检查指定类型和数量的邮件。
    
    Args:
        message_type (str): 邮件类型，可选值包括 "All", "Unseen", "Seen", "Recent", "Answered", "Flagged"
        count (int): 要检索的邮件数量
        
    Returns:
        List[Dict]: 包含邮件信息的字典列表

    必填参数:
        account (str): 邮箱账号
        password (str): 授权码/密码

    可选参数:
        imap_server (str, optional): 自定义IMAP服务器地址；未提供时自动匹配
    """
    if not account or not password:
        raise ValueError("account 和 password 为必填参数")
    email_163 = Email(
        imap=imap_server or get_imap_server(account),
        account=account,
        password=password,
    )
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

def save_attachment(
    file_name: str,
    account: str,
    password: str,
    save_path: str = '',
    imap_server: Optional[str] = None,
) -> str:
    """
    保存指定的附件到指定路径。
    
    Args:
        file_name (str): 要保存的附件文件名
        save_path (str): 保存路径，默认为空（当前目录）
        
    Returns:
        str: 保存的文件路径

    必填参数:
        account (str): 邮箱账号
        password (str): 授权码/密码

    可选参数:
        imap_server (str, optional): 自定义IMAP服务器地址；未提供时自动匹配
    """
    if not account or not password:
        raise ValueError("account 和 password 为必填参数")
    email_163 = Email(
        imap=imap_server or get_imap_server(account),
        account=account,
        password=password,
        file_save_path=save_path,
    )
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

def send_text_email(
    to_addr: Union[str, List[str]],
    subject: str,
    content: str,
    account: str,
    password: str,
    cc_addr: Union[str, List[str], None] = None,
    smtp_server: Optional[str] = None,
) -> Dict[str, str]:
    """
    发送纯文本邮件
    
    Args:
        to_addr (str or list): 收件人邮箱地址，可以是单个字符串或字符串列表
        subject (str): 邮件主题
        content (str): 邮件正文内容
        cc_addr (str or list, optional): 抄送人邮箱地址，可以是单个字符串或字符串列表
        
    Returns:
        dict: 包含发送状态和消息的字典

    必填参数:
        account (str): 发送者邮箱账号
        password (str): 授权码/密码

    可选参数:
        smtp_server (str, optional): 自定义SMTP服务器地址；未提供时自动匹配
    """
    if not account or not password:
        raise ValueError("account 和 password 为必填参数")
    sender = EmailSender(
        account=account,
        password=password,
        smtp_server=smtp_server or get_smtp_server(account),
    )
    return sender.send_text_email(to_addr, subject, content, cc_addr)

def send_html_email(
    to_addr: Union[str, List[str]],
    subject: str,
    html_content: str,
    account: str,
    password: str,
    cc_addr: Union[str, List[str], None] = None,
    smtp_server: Optional[str] = None,
) -> Dict[str, str]:
    """
    发送HTML格式邮件
    
    Args:
        to_addr (str or list): 收件人邮箱地址，可以是单个字符串或字符串列表
        subject (str): 邮件主题
        html_content (str): HTML格式的邮件正文内容
        cc_addr (str or list, optional): 抄送人邮箱地址，可以是单个字符串或字符串列表
        
    Returns:
        dict: 包含发送状态和消息的字典

    必填参数:
        account (str): 发送者邮箱账号
        password (str): 授权码/密码

    可选参数:
        smtp_server (str, optional): 自定义SMTP服务器地址；未提供时自动匹配
    """
    if not account or not password:
        raise ValueError("account 和 password 为必填参数")
    sender = EmailSender(
        account=account,
        password=password,
        smtp_server=smtp_server or get_smtp_server(account),
    )
    return sender.send_html_email(to_addr, subject, html_content, cc_addr)

def send_email_with_attachment(
    to_addr: Union[str, List[str]],
    subject: str,
    content: str,
    attachment_paths: Union[str, List[str]],
    account: str,
    password: str,
    cc_addr: Union[str, List[str], None] = None,
    is_html: bool = False,
    smtp_server: Optional[str] = None,
) -> Dict[str, str]:
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

    必填参数:
        account (str): 发送者邮箱账号
        password (str): 授权码/密码

    可选参数:
        smtp_server (str, optional): 自定义SMTP服务器地址；未提供时自动匹配
    """
    if not account or not password:
        raise ValueError("account 和 password 为必填参数")
    sender = EmailSender(
        account=account,
        password=password,
        smtp_server=smtp_server or get_smtp_server(account),
    )
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