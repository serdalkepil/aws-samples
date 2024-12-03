import { S3Event } from 'aws-lambda';
import { S3, DynamoDB } from 'aws-sdk';

const s3 = new S3();
const dynamoDB = new DynamoDB.DocumentClient();

export const handler = async (event: S3Event) => {
  try {
    // Extract bucket and key from the event
    const bucket = event.Records[0].s3.bucket.name;
    const key = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '));

    // Get object metadata
    const metadata = await s3.headObject({ Bucket: bucket, Key: key }).promise();

    // Store metadata in DynamoDB
    await dynamoDB.put({
      TableName: process.env.DYNAMODB_TABLE!,
      Item: {
        imageId: key,
        size: metadata.ContentLength,
        contentType: metadata.ContentType,
        lastModified: metadata.LastModified.toISOString()
      }
    }).promise();

    console.log(`Processed image: ${key}`);
    return { status: 'success' };
  } catch (error) {
    console.error('Error processing image:', error);
    throw error;
  }
};