# Option 2: Automate Snowpipe with AWS Lambda

AWS Lambda is a compute service that runs when triggered by an event and executes code that has been loaded into the system. You can adapt the sample Python code provided in this topic and create a Lambda
function that calls the Snowpipe REST API to load data from your external stage (i.e. S3 bucket; Azure containers are not supported). The function is deployed to your AWS account, where it is hosted. Events
you define in Lambda (e.g. when files in your S3 bucket are updated) invoke the Lambda function and run the Python code.

This topic describes the steps necessary to configure a Lambda function to automatically load data in micro-batches continuously using Snowpipe.

Note

This topic assumes you have configured Snowpipe using the instructions in [Data loading preparation using the Snowpipe REST API](/user-guide/data-load-snowpipe-rest-gs).

## Step 1: Write Python code invoking the Snowpipe REST API

**Sample Python code**

Copy code

```
from __future__ import print_function
from snowflake.ingest import SimpleIngestManager
from snowflake.ingest import StagedFile
from requests import HTTPError
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PrivateFormat
from cryptography.hazmat.primitives.serialization import NoEncryption
from cryptography.hazmat.backends import default_backend

import os

with open("./rsa_key.p8", 'rb') as pem_in:
  pemlines = pem_in.read()
  private_key_obj = load_pem_private_key(pemlines,
  os.environ['PRIVATE_KEY_PASSPHRASE'].encode(),
  default_backend())

private_key_text = private_key_obj.private_bytes(
  Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()).decode('utf-8')
# Assume the public key has been registered in Snowflake:
# private key in PEM format

# List of files in the stage specified in the pipe definition
ingest_manager = SimpleIngestManager(account='<account_identifier>',
                   host='<account_identifier>.snowflakecomputing.com',
                   user='<user_login_name>',
                   pipe='<db_name>.<schema_name>.<pipe_name>',
                   private_key=private_key_text)

def handler(event, context):
  for record in event['Records']:
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    print("Bucket: " + bucket + " Key: " + key)
    # List of files in the stage specified in the pipe definition
    # wrapped into a class
    staged_file_list = []
    staged_file_list.append(StagedFile(key, None))

    print('Pushing file list to ingest REST API')
    resp = ingest_manager.ingest_files(staged_file_list)
```

Note

The sample code does not account for error handling. For example, it does not retry failed `ingest_manager` calls.

Before using the sample code, make the following changes:

1. Update the security parameter:

   `private_key=""" / -----BEGIN RSA PRIVATE KEY----- / ... / -----END RSA PRIVATE KEY----- """`
   :   Specifies the content of the private key file you created in [Use key pair authentication & key rotation](/user-guide/data-load-snowpipe-rest-gs#label-configuring-rsa-authentication-keys) (in [Data loading preparation using the Snowpipe REST API](/user-guide/data-load-snowpipe-rest-gs)).

   Specify the passphrase for decrypting the private key file using the `PRIVATE_KEY_PASSPHRASE` environment variable:

   - Linux or macOS:

     Copy code

     ```
     export PRIVATE_KEY_PASSPHRASE='<passphrase>'
     ```
   - Windows:

     Copy code

     ```
     set PRIVATE_KEY_PASSPHRASE='<passphrase>'
     ```
2. Update the session parameters:

   `account='<account_identifier>'`
   :   Specify the unique identifier for your account (provided by Snowflake). See the `host` description.

   `host='<account_identifier>.snowflakecomputing.com'`
   :   Specify the unique hostname for your Snowflake account.

       The preferred format of the account identifier is as follows:

       `organization_name-account_name`
       :   Names of your Snowflake organization and account. For details, see [Format 1 (preferred): Account name in your organization](/user-guide/admin-account-identifier#label-account-name).

       Alternatively, specify your *account locator*, along with the [region](/user-guide/intro-regions) and [cloud platform](/user-guide/intro-cloud-platforms) where the account is hosted, if required. For details, see [Format 2: Account locator in a region](/user-guide/admin-account-identifier#label-account-locator).

   `user='<user_login_name>'`
   :   Specifies the login name of the Snowflake user that will run the Snowpipe code.

   `pipe='<db_name>.<schema_name>.<pipe_name>'`
   :   Specifies the fully-qualified name of the pipe to use to load the data, in the form of `<db_name>.<schema_name>.<pipe_name>`.
3. Specify the path to your files to import in the file objects list:

   `staged_file_list = []`
   :   The path you specify must be relative to the stage where the files are located. Include the complete name for each file, including the file extension. For example, a CSV file that is
       gzip-compressed might have the extension `.csv.gz`.
4. Save the file in a convenient location.

The remaining instructions in this topic assume the file name to be `SnowpipeLambdaCode.py`.

## Step 2: Create a Lambda function deployment package

Complete the following instructions to build a Python runtime environment for Lambda and add the Snowpipe code you adapted in [Step 1: Write Python Code Invoking the Snowpipe REST API](#step-1-write-python-code-invoking-the-snowpipe-rest-api) (in this topic).
For more information about these steps, see the [AWS Lambda deployment package documentation](http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-deployment-pkg.html) (see the instructions for
Python).

Important

The scripts in the following steps are a representative example and assume that you are creating an AWS EC2 Linux instance based on an Amazon Machine Instance (AMI) that uses the YUM package manager, which depends on RPM. If you select a Debian-based Linux AMI, please update your scripts accordingly.

1. Create an AWS EC2 Linux instance by completing the [AWS EC2 instructions](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-launch-instance). This instance will provide the
   compute resources to run the Snowpipe code.
2. Copy the Snowpipe code file to your new AWS EC2 instance using SCP (Secure Copy):

   Copy code

   ```
   scp -i key.pem /<path>/SnowpipeLambdaCode.py ec2-user@<machine>.<region_id>.compute.amazonaws.com:~/SnowpipeLambdaCode.py
   ```

   Where:

   - `<path>` is the path to your local `SnowpipeLambdaCode.py` file.
   - `<machine>.<region_id>` is the DNS name of the EC2 instance (e.g. `ec2-54-244-54-199.us-west-2.compute.amazonaws.com`).

     The DNS name is displayed on the **Instances** screen in the Amazon EC2 console.
3. Connect to the EC2 instance using SSH (Secure SHell):

   Copy code

   ```
   ssh -i key.pem ec2-user@<machine>.<region_id>.compute.amazonaws.com
   ```
4. Install Python and related libraries on the EC2 instance:

   Copy code

   ```
   sudo yum install -y gcc zlib zlib-devel openssl openssl-devel

   wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz

   tar -xzvf Python-3.6.1.tgz

   cd Python-3.6.1 && ./configure && make

   sudo make install

   sudo /usr/local/bin/pip3 install virtualenv

   /usr/local/bin/virtualenv ~/shrink_venv

   source ~/shrink_venv/bin/activate

   pip install Pillow

   pip install boto3

   pip install requests

   pip install snowflake-ingest
   ```
5. Create the .zip deployment package (`Snowpipe.zip`):

   Copy code

   ```
   cd $VIRTUAL_ENV/lib/python3.6/site-packages

   zip -r9 ~/Snowpipe.zip .

   cd ~

   zip -g Snowpipe.zip SnowpipeLambdaCode.py
   ```

## Step 3: Create an AWS IAM role for Lambda

Follow the [AWS Lambda documentation](http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-create-iam-role.html) to create an IAM role to execute the Lambda function.

Record the [IAM Amazon Resource Name (ARN)](http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-arns) for the role. You will use it in the next step.

## Step 4: Create the Lambda function

Create the Lambda function by uploading the `.zip` deployment package you created in [Step 2: Create a Lambda Function Deployment Package](#step-2-create-a-lambda-function-deployment-package) (in this topic):

> Copy code
>
> ```
> aws lambda create-function \
> --region us-west-2 \
> --function-name IngestFile \
> --zip-file fileb://~/Snowpipe.zip \
> --role arn:aws:iam::<aws_account_id>:role/lambda-s3-execution-role \
> --handler SnowpipeLambdaCode.handler \
> --runtime python3.6 \
> --profile adminuser \
> --timeout 10 \
> --memory-size 1024
> ```

For `--role`, specify the role ARN you recorded in [Step 3: Create an AWS IAM Role for Lambda](#step-3-create-an-aws-iam-role-for-lambda) (in this topic).

Record the ARN for the new function from the output. You will use it in the next step.

## Step 5: Allow calls to the Lambda function

Grant S3 the permissions required to invoke your function.

For `--source-arn`, specify the function ARN you recorded in [Step 4: Create the Lambda Function](#step-4-create-the-lambda-function) (in this topic).

> Copy code
>
> ```
> aws lambda add-permission \
> --function-name IngestFile \
> --region us-west-2 \
> --statement-id enable-ingest-calls \
> --action "lambda:InvokeFunction" \
> --principal s3.amazonaws.com \
> --source-arn arn:aws:s3:::<SourceBucket> \
> --source-account <aws_account_id> \
> --profile adminuser
> ```

## Step 6: Register the Lambda notification event

Register a Lambda notification event by completing the [Amazon S3 Event Notifications](http://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html) instructions. In the input field, specify the
function ARN you recorded in [Step 4: Create the Lambda Function](#step-4-create-the-lambda-function) (in this topic).
