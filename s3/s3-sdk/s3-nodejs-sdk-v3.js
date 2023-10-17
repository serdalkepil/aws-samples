import {
    CreateBucketCommand,
    DeleteBucketCommand,
    ListBucketsCommand,
    S3Client,
  } from "@aws-sdk/client-s3";
  
  const wait = async (milliseconds) => {
    return new Promise((resolve) => setTimeout(resolve, milliseconds));
  };
  
  export const main = async () => {
    const client = new S3Client({});
    const now = Date.now();
    const BUCKET_NAME = `easy-bucket-${now.toString()}`;
  
    const createBucketCommand = new CreateBucketCommand({ Bucket: BUCKET_NAME });
    const listBucketsCommand = new ListBucketsCommand({});
    const deleteBucketCommand = new DeleteBucketCommand({ Bucket: BUCKET_NAME });
  
    try {
      console.log(`Creating bucket ${BUCKET_NAME}.`);
      await client.send(createBucketCommand);
      console.log(`${BUCKET_NAME} created`);
  
      await wait(2000);
  
      console.log(`Here are your buckets:`);
      const { Buckets } = await client.send(listBucketsCommand);
      Buckets.forEach((bucket) => {
        console.log(` • ${bucket.Name}`);
      });
  
      await wait(2000);
  
      console.log(`Deleting bucket ${BUCKET_NAME}.`);
      await client.send(deleteBucketCommand);
      console.log(`${BUCKET_NAME} deleted`);
    } catch (err) {
      console.error(err);
    }
  };
  