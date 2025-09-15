# AWS IAM Demo with AWS CLI

This demo shows how to use AWS CLI for a complete IAM workflow:

- Create a user  
- Create a limited S3 access policy  
- Create a role  
- Allow the user to assume the role  
- Verify identity before and after assuming the role  
- Generate and use temporary credentials  

---

## 1. Create IAM User

```bash
aws iam create-user --user-name DemoUser
```

This creates an IAM user named **DemoUser**.  
You can later attach access keys for CLI/API access.

```bash
aws iam create-access-key --user-name DemoUser
```

---

## 2. Create a Limited S3 Access Policy

Create a JSON file `s3_limited_policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::demo-bucket"
    },
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::demo-bucket/*"
    }
  ]
}
```

This policy allows the user/role to **list the bucket** and **read objects** in `demo-bucket`.

Create the policy in IAM:

```bash
aws iam create-policy   --policy-name DemoS3LimitedAccess   --policy-document file://s3_limited_policy.json
```

---

## 3. Create an IAM Role

First, create a **trust policy** (`trust-policy.json`):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<ACCOUNT_ID>:user/DemoUser"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

This defines **who is allowed to assume the role**. In this case, the IAM user `DemoUser`.

Create the role:

```bash
aws iam create-role   --role-name DemoS3Role   --assume-role-policy-document file://trust-policy.json
```

Attach the S3 policy:

```bash
aws iam attach-role-policy   --role-name DemoS3Role   --policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/DemoS3LimitedAccess
```

---

## 4. Allow User to Assume the Role

Create a policy `assume-role-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::<ACCOUNT_ID>:role/DemoS3Role"
    }
  ]
}
```

Attach this inline policy to the user:

```bash
aws iam put-user-policy   --user-name DemoUser   --policy-name AllowAssumeDemoRole   --policy-document file://assume-role-policy.json
```

This allows the **DemoUser** to call `sts:AssumeRole` on the `DemoS3Role`.

---

## 5. Verify Identity as the User

Using the **DemoUser credentials**, check who you are:

```bash
aws sts get-caller-identity
```

Example output:

```json
{
  "UserId": "AIDAxxxxxxxxxxxx",
  "Account": "<ACCOUNT_ID>",
  "Arn": "arn:aws:iam::<ACCOUNT_ID>:user/DemoUser"
}
```

---

## 6. Assume the Role

```bash
aws sts assume-role   --role-arn arn:aws:iam::<ACCOUNT_ID>:role/DemoS3Role   --role-session-name DemoSession
```

This returns **temporary credentials**:

```json
{
  "Credentials": {
    "AccessKeyId": "ASIAxxxxxxxxxxxx",
    "SecretAccessKey": "xxxxxxxxxxxx",
    "SessionToken": "xxxxxxxxxxxx",
    "Expiration": "2025-09-15T12:00:00Z"
  },
  "AssumedRoleUser": {
    "AssumedRoleId": "AROAxxxxxxxxxxxx",
    "Arn": "arn:aws:sts::<ACCOUNT_ID>:assumed-role/DemoS3Role/DemoSession"
  }
}
```

---

## 7. Export Temporary Credentials

Export them to your environment:

```bash
export AWS_ACCESS_KEY_ID=ASIAxxxxxxxxxxxx
export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxx
export AWS_SESSION_TOKEN=xxxxxxxxxxxx
```

---

## 8. Verify Identity as Assumed Role

```bash
aws sts get-caller-identity
```

Example output:

```json
{
  "UserId": "AROAxxxxxxxxxxxx:DemoSession",
  "Account": "<ACCOUNT_ID>",
  "Arn": "arn:aws:sts::<ACCOUNT_ID>:assumed-role/DemoS3Role/DemoSession"
}
```

Now your CLI is running with the **role’s limited S3 access**.

---

## 9. Test S3 Access

Try listing the bucket:

```bash
aws s3 ls s3://demo-bucket/
```

This should succeed if the role is assumed correctly.  
Trying to access another bucket should fail due to the **limited policy**.

---

## Cleanup (Optional)

When done, you can clean up resources:

```bash
aws iam delete-user-policy --user-name DemoUser --policy-name AllowAssumeDemoRole
aws iam detach-role-policy --role-name DemoS3Role --policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/DemoS3LimitedAccess
aws iam delete-role --role-name DemoS3Role
aws iam delete-policy --policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/DemoS3LimitedAccess
aws iam delete-user --user-name DemoUser
```

---

## Summary

- **DemoUser**: IAM user without direct S3 permissions  
- **DemoS3Role**: IAM role with limited S3 access  
- **Temporary credentials**: Obtained via `sts:AssumeRole`  
- Verified with `aws sts get-caller-identity` before and after assuming role  
