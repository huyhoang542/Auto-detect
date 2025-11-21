# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

# ==================== CẤU HÌNH MAIL (Đọc từ Biến Môi trường) ====================
# Đặt các giá trị mặc định, ưu tiên đọc từ Biến Môi trường
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'your_project_email@gmail.com')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD', 'DEFAULT_TEST_PASSWORD') 
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL', 'admin_alert@yourcompany.com')
# =================================================================================

def send_alert_email(alert_data):
    """Gửi email cảnh báo dựa trên dữ liệu alert_data."""
    
    subject = f"[CRITICAL ALERT - SEV {alert_data.get('severity')}] IP Blocked: {alert_data.get('ip_address')}"
    
    # Chỉ gửi Metadata quan trọng nhất (Content Scrubbing)
    body = f"""
    -- SECURITY ALERT --
    
    TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    SEVERITY: {alert_data.get('severity')}
    DETECTION TYPE: {alert_data.get('detection_type')}
    
    IP ADDRESS: {alert_data.get('ip_address')}
    USERNAME: {alert_data.get('username', 'N/A')}
    
    REASON: {alert_data.get('reason')}
    
    ACTION TAKEN: This IP HAS BEEN FLAGGED/BLOCKED.
    """
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        # Kiểm tra nếu chưa thiết lập mật khẩu trong môi trường
        if SENDER_PASSWORD == 'DEFAULT_TEST_PASSWORD' or not SENDER_PASSWORD:
            print("EMAIL SEND ABORTED: SENDER_PASSWORD not set in environment variable.")
            return False

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() 
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"EMAIL ALERT SENT successfully to {RECEIVER_EMAIL}")
        return True
    except Exception as e:
        print(f"EMAIL SEND ERROR: Failed to send email. Check SMTP settings/App Password. {e}")
        return False

if __name__ == '__main__':
    pass
