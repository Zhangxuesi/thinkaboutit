import schedule
import time
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# 设置发送邮件的相关信息
email_user = 'zxs7240823@sohu.com'  # 你的邮箱地址
email_password = '1W4V0DMXKO75'  # 你的邮箱密码或授权码
email_send_to = '5355776@qq.com'  # 收件人邮箱地址
subject = 'Scheduled Email with Attachments'  # 邮件主题
body = 'This is a scheduled email with attachments.'  # 邮件正文
attachments = ['D:\PycharmProjects\KILLRUNNINGCASE.xlsx']  # 要作为附件的文件路径列表

# zxs7240823@sohu.com
# 1qaz@WSX
# POP3服务:pop3.sohu.com
# SMTP服务:smtp.sohu.com
# IMAP服务:imap.sohu.com
def send_email():
    # 创建一个邮件对象
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send_to
    msg['Subject'] = subject

    # 邮件正文内容
    msg.attach(MIMEText(body, 'plain'))

    # 添加附件
    for file in attachments:
        attachment = open(file, 'rb')  # 以二进制模式打开文件

        # 实例化MIMEBase对象
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(file)}')

        msg.attach(part)
        attachment.close()

    try:
        # 登录至SMTP服务器并发送邮件
        server = smtplib.SMTP('smtp.sohu.com', 25)  # 邮件服务器地址和端口（此处以Example为例）
        # server.starttls()  # 启动TLS加密模式
        server.login(email_user, email_password)
        server.sendmail(email_user, email_send_to, msg.as_string())
        server.quit()

        print(f'Email sent to {email_send_to} successfully!')

    except Exception as e:
        print(f'Failed to send email to {email_send_to}. Error: {str(e)}')


# 调度任务，定时在指定时间发送邮件
def schedule_email(time_to_send):
    schedule.every().day.at(time_to_send).do(send_email)  # 每天在指定时间执行发送邮件任务
    while True:
        schedule.run_pending()  # 检查任务是否需要运行
        time.sleep(30)  # 暂停1秒，避免频繁检测


if __name__ == "__main__":
    time_to_send = "11:29"  # 设置发送邮件的时间（24小时格式）
    schedule_email(time_to_send)  # 开始调度任务