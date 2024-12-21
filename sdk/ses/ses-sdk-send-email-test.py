import boto3
from botocore.exceptions import ClientError

def send_ses_email(sender_email, recipient_email, subject, body_text, body_html=None):
    """
    Send an email using Amazon SES in the Ireland region.
    
    :param sender_email: Email address of the sender
    :param recipient_email: Email address of the recipient
    :param subject: Email subject line
    :param body_text: Plain text version of the email body
    :param body_html: Optional HTML version of the email body
    :return: Message ID if successful, None otherwise
    """
    # Create a new SES resource and specify region
    ses_client = boto3.client('ses', region_name='eu-west-1', aws_access_key_id='AKIADSFFGSDDSFWERSDFDSFS', aws_secret_access_key='sfsdFSFWEDSFDSFLWEKdljfksdjfjwkej')
    
    # Prepare the email message
    email_message = {
        'Source': sender_email,
        'Destination': {
            'ToAddresses': [recipient_email]
        },
        'Message': {
            'Subject': {
                'Data': subject,
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': body_text,
                    'Charset': 'UTF-8'
                }
            }
        }
    }
    
    # Add HTML body if provided
    if body_html:
        email_message['Message']['Body']['Html'] = {
            'Data': body_html,
            'Charset': 'UTF-8'
        }
    
    try:
        # Attempt to send the email
        response = ses_client.send_email(**email_message)
        print(f"Email sent successfully! Message ID: {response['MessageId']}")
        return response['MessageId']
    
    except ClientError as e:
        # Print any errors encountered
        print(f"Email sending failed. Error: {e.response['Error']['Message']}")
        return None

def main():
    # Configuration - REPLACE THESE WITH YOUR ACTUAL VALUES
    SENDER_EMAIL = 'name@sender.com'
    RECIPIENT_EMAIL = 'recipient@mail.com'
    
    # Test email details
    subject = 'AWS SES Email Credentials Test'
    body_text = 'This is a test email sent from AWS SES in the Ireland region.'
    body_html = '''
    <html>
        <body>
            <h1>AWS SES Email Test</h1>
            <p>This is a <strong>test email</strong> sent from Amazon SES in the Ireland region.</p>
        </body>
    </html>
    '''
    
    # Send the email
    send_ses_email(
        sender_email=SENDER_EMAIL, 
        recipient_email=RECIPIENT_EMAIL, 
        subject=subject, 
        body_text=body_text,
        body_html=body_html
    )

if __name__ == '__main__':
    main()
