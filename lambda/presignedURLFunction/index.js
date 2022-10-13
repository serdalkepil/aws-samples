'use strict';

const AWS = require('aws-sdk');
const s3 = new AWS.S3({signatureVersion: 'v4'});

exports.handler = (event, context, callback) => {
  const bucket = event['s3_bucket'];
  if (!bucket) {
    callback(new Error(`S3 bucket not set`));
  }
  
  const key = event['object_key'];
  if (!key) {
    callback(new Error('S3 object key missing'));
    return;
  }
  
  const signedURLExpireSeconds =  event['duration'];

  const params = {'Bucket': bucket, 'Key': key, Expires: signedURLExpireSeconds};

  s3.getSignedUrl('getObject', params, (error, url) => {
    if (error) {
      callback(error);
    } else {
      callback(null, {url: url});
    }
  });
};