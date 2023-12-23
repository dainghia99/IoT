import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Thông tin tài khoản email
sender_email = "midvip99@gmail.com"
sender_password = "hanhulanh"

# Địa chỉ email người nhận
receiver_email = "lehonganh19022003@gmail.com"

# Tạo thông điệp email
subject = "Ngu như con bò"
body = "Bẩn thối"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

# Kết nối đến máy chủ SMTP của Gmail
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    
    # Đăng nhập vào tài khoản email của bạn
    server.login(sender_email, sender_password)
    
    # Gửi email
    server.sendmail(sender_email, receiver_email, message.as_string())

print("Email đã được gửi thành công.")
