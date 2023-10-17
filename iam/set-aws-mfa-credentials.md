# How to set AWS multi-factor authentication (MFA) credentials

## Pre-test

In a pre-test, verify that EC2 cannot be launched without multi-factor authentication.

1. :pencil2: Specify an AWS AMI to launch.
   Example:

    ```console
    export AWS_IMAGE_ID=ami-0d592b9373fad0e2c
    ```

1. :pencil2: Identify the key pair to be used with the running image.
   See [AWS Console EC2 Key pairs](https://console.aws.amazon.com/ec2/v2/home?#KeyPairs:).
   Example:

    ```console
    export SENZING_AWS_KEYPAIR=aws-default-key-pair
    ```

1. Try launching the image.
   **NOTE:** As a pre-test, this should fail.
   Example:

    ```console
    aws ec2 run-instances \
      --image-id ${AWS_IMAGE_ID} \
      --count 1 \
      --instance-type t2.micro \
      --key-name ${SENZING_AWS_KEYPAIR}
    ```

1. Verify EC2 is not running.
   1. [AWS EC2 console](https://console.aws.amazon.com/ec2/v2/home?#Instances:)

## Obtain AWS session credentials

1. :pencil2: Identify the AWS multi-factor authentication serial number for the device supplying the MFA token.
   Registered devices can be found at
   [AWS My security credentials](https://console.aws.amazon.com/iam/home?#/security_credentials)
   Example:

    ```console
    export AWS_MFA_SERIAL_NUMBER="arn:aws:iam::nnnnnnnnnnnn:mfa/xxxxxxxx"
    ```

1. :pencil2: Get MFA token from the device supplying the MFA token.
   **Note:** This token is short lived;  perhaps only one minute duration.
   So the step performed after this step must be performed immediately afterwards to use a valid token value.
   Example:

    ```console
    export AWS_MFA_TOKEN_CODE=nnnnnn
    ```

1. Get session information from AWS and place into `~/aws-sts-get-session-token.json` file.
   Example:

    ```console
    aws sts get-session-token \
      --serial-number ${AWS_MFA_SERIAL_NUMBER} \
      --token-code ${AWS_MFA_TOKEN_CODE} \
      > ~/aws-sts-get-session-token.json
    ```

1. Parse values out of AWS session information and place in environment variables.
   Example:

    ```console
    export AWS_ACCESS_KEY_ID=$(jq --raw-output ".Credentials.AccessKeyId" ~/aws-sts-get-session-token.json)
    export AWS_SECRET_ACCESS_KEY=$(jq --raw-output ".Credentials.SecretAccessKey" ~/aws-sts-get-session-token.json)
    export AWS_SESSION_TOKEN=$(jq --raw-output ".Credentials.SessionToken" ~/aws-sts-get-session-token.json)
    ```

1. :thinking: **Optional:** View expiration time of AWS session.
   Example:

    ```console
    echo "AWS token expires: $(jq --raw-output ".Credentials.Expiration" ~/aws-sts-get-session-token.json)"
    ```

1. :thinking: **Optional:** View AWS session token.
   Example:

    ```console
    echo ${AWS_SESSION_TOKEN}
    ```

## Launch EC2

1. :pencil2: Launch EC2.
   This should now work because environment variables contain credentials for authentication.
   Example:

    ```console
    aws ec2 run-instances \
      --image-id ${AWS_IMAGE_ID} \
      --count 1 \
      --instance-type t2.micro \
      --key-name ${SENZING_AWS_KEYPAIR}
    ```

1. Verify EC2 is running.
   1. [AWS EC2 console](https://console.aws.amazon.com/ec2/v2/home?#Instances:)
