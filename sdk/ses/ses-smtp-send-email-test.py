import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_ses_smtp_email(
        smtp_username,
        smtp_password,
        sender_email,
        recipient_email,
        subject,
        body_text,
        body_html=None
):
    """
    Send an email using AWS SES SMTP interface.

    :param smtp_username: AWS SES SMTP username
    :param smtp_password: AWS SES SMTP password
    :param sender_email: Email address of the sender
    :param recipient_email: Email address of the recipient
    :param subject: Email subject line
    :param body_text: Plain text version of the email body
    :param body_html: Optional HTML version of the email body
    """
    # AWS SES SMTP Settings for Ireland Region
    SMTP_HOST = 'email-smtp.eu-west-1.amazonaws.com'
    SMTP_PORT = 587  # TLS port

    try:
        # Create a multipart message
        message = MIMEMultipart('alternative')
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Attach plain text part
        text_part = MIMEText(body_text, 'plain')
        message.attach(text_part)

        # Attach HTML part if provided
        if body_html:
            html_part = MIMEText(body_html, 'html')
            message.attach(html_part)

        # Create SMTP session
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            # Start TLS for security
            server.starttls()

            # Login to the SMTP server
            server.login(smtp_username, smtp_password)

            # Send email
            server.sendmail(
                sender_email,
                recipient_email,
                message.as_string()
            )

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

def main():
    # AWS SES SMTP Credentials - REPLACE WITH YOUR ACTUAL CREDENTIALS
    SMTP_USERNAME = 'AKIASDKFHESDF7747474'
    SMTP_PASSWORD = 'KSDHFKWLELKJDFLKSDJkjfhkshdfj23423'

    # Email Configuration
    SENDER_EMAIL = 'sender@company.com'
    RECIPIENT_EMAIL = 'recipient@test.com'

    # Email Content
    subject = 'AWS SES SMTP Email Test'
    body_text = 'This is a test email sent using AWS SES SMTP in the Ireland region.'
    body_html = '''
    <html>
        <body>
            <h1>AWS SES SMTP Email Test</h1>
            <p>This is a <strong>test email</strong> sent using AWS SES SMTP in the Ireland region.</p>
        </body>
    </html>
    '''

    # Send the email
    send_ses_smtp_email(
        smtp_username=SMTP_USERNAME,
        smtp_password=SMTP_PASSWORD,
        sender_email=SENDER_EMAIL,
        recipient_email=RECIPIENT_EMAIL,
        subject=subject,
        body_text=body_text,
        body_html=body_html
    )

if __name__ == '__main__':
    main()