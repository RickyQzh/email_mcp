"""
163邮箱配置文件
"""
import os
from dotenv import load_dotenv

# 尝试加载.env文件（如果存在）
load_dotenv()

# 邮箱服务器配置
IMAP_SERVER = os.environ.get('EMAIL_IMAP_SERVER', 'imap.163.com')
SMTP_SERVER = os.environ.get('EMAIL_SMTP_SERVER', 'smtp.163.com')
ACCOUNT = os.environ.get('EMAIL_ACCOUNT', '13831044889@163.com')
PASSWORD = os.environ.get('EMAIL_PASSWORD', 'MFgnfTKLdcX8JcMd')