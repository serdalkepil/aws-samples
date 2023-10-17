# How to set AWS environment variables

Amazon Web Services (AWS) command-line interface (CLI) supports specific environment variables.
These environment variables are listed at
[Environment variables to configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)

In python scripts using the
[AWS boto3](https://aws.amazon.com/sdk-for-python/)
library, there is a
[list of environment variables](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#using-environment-variables)
that are used by the library.

If using `AWS_SESSION_TOKEN`, a session will need to be created and environment variable values will need to use the session information.

## AWS Session

### Create AWS session credentials

1. Get session information from AWS and place into `~/aws-sts-get-session-token.json` file.
   Example:

    ```console
    aws sts get-session-token \
      > ~/aws-sts-get-session-token.json
    ```

### Create AWS MFA session credentials

1. :pencil2: Identify the AWS multi-factor authentication serial number for the device supplying the MFA token.
   Registered devices can be found at
   [AWS My security credentials](https://console.aws.amazon.com/iam/home?#/security_credentials)
   Example:

    ```console
    export AWS_MFA_SERIAL_NUMBER="arn:aws:iam::nnnnnnnnnnnn:mfa/xxxxxxxx"
    ```

   If defined in `~/.aws/config`, run:

    ```console
    export AWS_MFA_SERIAL_NUMBER=$(aws configure get default.mfa_serial)
    ```

1. :pencil2: Get MFA token from the device supplying the MFA token.
   It is usually a 6-digit number.
   **Note:** This token is short lived;
   perhaps only one minute duration.
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

## AWS environment variables

### AWS_ACCESS_KEY_ID

1. Pull information from `~/.aws/credentials`
   Example:

    ```console
    export AWS_ACCESS_KEY_ID=$(aws configure get default.aws_access_key_id)
    ```

1. For a [session](#aws-session),
   pull information from `~/aws-sts-get-session-token.json`,
   a file created in the [AWS Session](#aws-session) section.
   Example:

    ```console
    export AWS_ACCESS_KEY_ID=$(jq --raw-output ".Credentials.AccessKeyId" ~/aws-sts-get-session-token.json)
    ```

1. References:
    1. [Usage](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#aws_access_key_id)

### AWS_DEFAULT_REGION

1. Pull information from `~/.aws/config`
   Example:

    ```console
    export AWS_DEFAULT_REGION=$(aws configure get default.region)
    ```

1. References:
    1. [Usage](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#aws_default_region)

### AWS_SECRET_ACCESS_KEY

1. Pull information from `~/.aws/credentials`
   Example:

    ```console
    export AWS_SECRET_ACCESS_KEY=$(aws configure get default.aws_secret_access_key)
    ```

1. For a [session](#aws-session),
   pull information from `~/aws-sts-get-session-token.json`,
   a file created in the [AWS Session](#aws-session) section.
   Example:

    ```console
    export AWS_SECRET_ACCESS_KEY=$(jq --raw-output ".Credentials.SecretAccessKey" ~/aws-sts-get-session-token.json)
    ```

1. References:
    1. [Usage](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#aws_secret_access_key)

### AWS_SESSION_TOKEN

1. For a [session](#aws-session),
   pull information from `~/aws-sts-get-session-token.json`,
   a file created in the [AWS Session](#aws-session) section.
   Example:

    ```console
    export AWS_SESSION_TOKEN=$(jq --raw-output ".Credentials.SessionToken" ~/aws-sts-get-session-token.json)
    ```

1. References:
    1. [Usage](https://github.com/Senzing/knowledge-base/blob/main/lists/environment-variables.md#aws_session_token)

## Non-AWS environment variables

### AWS_MFA_SERIAL_NUMBER

1. Pull information from `~/.aws/config`
   Example:

    ```console
    export AWS_MFA_SERIAL_NUMBER=$(aws configure get default.mfa_serial)
    ```

### AWS_MFA_TOKEN_CODE

1. :pencil2: Get MFA token from the device supplying the MFA token.
   **Note:** This token is short lived;  perhaps only one minute duration.
   So the step performed after this step must be performed immediately afterwards to use a valid token value.
   Example:

    ```console
    export AWS_MFA_TOKEN_CODE=nnnnnn
    ```
