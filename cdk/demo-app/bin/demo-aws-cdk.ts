import { fileURLToPath } from 'url';
import { dirname } from 'path';
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DemoAwsCdkStack } from '../lib/demo-aws-cdk-stack.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = new cdk.App();
new DemoAwsCdkStack(app, 'DemoAwsCdkStack', {
  env: { 
    account: process.env.CDK_DEFAULT_ACCOUNT, 
    region: process.env.CDK_DEFAULT_REGION 
  }
});