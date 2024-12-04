import json
import os
import urllib3
import logging
import boto3
from typing import List, Dict

# Configure logging based on environment
def configure_logging():
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

# Initialize logger
logger = configure_logging()

# Initialize SNS client
sns_client = boto3.client('sns')

def check_url_health(url: str) -> Dict:
    """
    Check the health of a given URL

    :param url: URL to check
    :return: Dictionary with health check result
    """
    http = urllib3.PoolManager()

    try:
        response = http.request('GET', url, timeout=5.0)

        return {
            'url': url,
            'status_code': response.status,
            'is_healthy': response.status == 200,
            'message': 'URL is healthy' if response.status == 200 else f'Unhealthy status: {response.status}'
        }
    except Exception as e:
        return {
            'url': url,
            'status_code': None,
            'is_healthy': False,
            'message': f'Error checking URL: {str(e)}'
        }

def send_sns_alert(unhealthy_urls: List[Dict]) -> None:
    """
    Send SNS alert for unhealthy URLs

    :param unhealthy_urls: List of unhealthy URL check results
    """
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
    environment = os.environ.get('ENVIRONMENT', 'Unknown')

    if not sns_topic_arn:
        logger.error("SNS Topic ARN not configured")
        return

    # Construct alert message
    message = f"URL Health Check Failures in {environment.upper()} Environment:\n\n"
    for url_result in unhealthy_urls:
        message += f"URL: {url_result['url']}\n"
        message += f"Status: {url_result['message']}\n\n"

    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject=f'URL Health Check Alert - {environment.upper()}',
            Message=message
        )
        logger.info(f"SNS alert sent for {len(unhealthy_urls)} unhealthy URLs")
    except Exception as e:
        logger.error(f"Failed to send SNS alert: {str(e)}")

def lambda_handler(event, context):
    """
    Lambda handler to check health of multiple URLs

    :param event: Lambda event
    :param context: Lambda context
    :return: Health check results
    """
    # Log environment and configuration
    environment = os.environ.get('ENVIRONMENT', 'Unknown')
    logger.info(f"Running health check in {environment} environment")


    # Retrieve URLs from environment variable
    urls_str = os.environ.get('URLS_TO_CHECK', '[]')

    try:
        urls = json.loads(urls_str)
    except json.JSONDecodeError:
        logger.error(f"Invalid URL configuration: {urls_str}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Invalid URL configuration'})
        }

    # Perform health checks
    results = [check_url_health(url) for url in urls]

    # Filter unhealthy URLs
    unhealthy_urls = [result for result in results if not result['is_healthy']]
    print(f"Unhealthy URLs: {unhealthy_urls}")

    # Log results
    for result in results:
        log_method = logger.warning if not result['is_healthy'] else logger.info
        log_method(f"Health check for {result['url']}: {result['message']}")

    # Send SNS alert for unhealthy URLs
    if unhealthy_urls:
        send_sns_alert(unhealthy_urls)

    print(json.dumps(results))
    logger.info(f"Health check completed for {len(urls)} URLs")

    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }