import streamlit as st
import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    # 送信元と宛先のメールアドレス
    from_email = "hatakeyamamitstumu1120@gmail.com"  # 送信元メールアドレス
    to_email = to_email  # 宛先メールアドレス

    # メールの本文
    message = MIMEText(body)

    # メールの件名
    message["Subject"] = subject

    # メールの送信元と宛先
    message["From"] = from_email
    message["To"] = to_email

    # SMTPサーバーに接続してメールを送信
    with smtplib.SMTP("your_smtp_server.com", 587) as server:  # SMTPサーバーアドレスとポート番号
        server.starttls()  # TLSを使用して接続
        server.login(from_email, "hatakeyamamitstumu1120@gmail.com")  # 送信元メールアドレスとパスワード

        # メールを送信
        server.sendmail(from_email, to_email, message.as_string())

# Streamlitアプリ
def main():
    st.title("Email Sender App")
    
    # メール送信ボタンが押されたときの処理
    if st.button("Send Email"):
        # メール送信
        send_email("hatakeyamamitstumu1120@gmail.com", "Hello World", "Hello, this is the email body.")

        # 成功メッセージを表示
        st.success("Email sent successfully!")

if __name__ == "__main__":
    main()
