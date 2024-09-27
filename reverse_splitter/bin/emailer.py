import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')
SMTP_SENDER= os.environ.get('SMTP_SENDER')

def send_html_email(receiver_email, subject, html_content):
    s_name, s_email = SMTP_SENDER.split(',')
    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = formataddr((s_name, s_email))
    msg['To'] = receiver_email

    # Record the MIME type - text/html.
    part = MIMEText(html_content, 'html')

    # Attach parts into message container.
    msg.attach(part)

    # Send the message via SMTP server.
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(formataddr((s_name, s_email)), receiver_email, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
if __name__ == "__main__":
    receiver_email = "seantsusmilch@proton.me"
    subject = "Test Email"
    html_content = "<html><body><h1>This is a test email</h1></body></html>"

    send_html_email(receiver_email, subject, html_content)