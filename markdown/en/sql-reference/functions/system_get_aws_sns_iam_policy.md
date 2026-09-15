Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_AWS\_SNS\_IAM\_POLICY

Returns an AWS IAM policy statement that must be added to the Amazon SNS topic policy in order to grant the Amazon SQS messaging queue created by Snowflake to subscribe to the topic.

This function is used when automating Snowpipe using SQS notifications for S3 events. To avoid conflicts with existing SQS queues for the same *endpoint* (i.e. S3 bucket), creating an SNS topic for the bucket and subscribing all SQS queues to this topic enables SNS to publish event notifications for the bucket to multiple subscribers.

## Syntax

Copy code

```
SYSTEM$GET_AWS_SNS_IAM_POLICY( '<sns_topic_arn>' )
```

## Arguments

`sns_topic_arn`
:   Amazon Resource Name (ARN) of the SNS topic for your S3 bucket. The function returns an IAM policy for Snowflake’s SQS queue to subscribe to this topic.

## Usage notes

- All arguments are strings (i.e. they must be enclosed in single quotes).

## Examples

Return an IAM policy for a specified SNS topic ARN:

> Copy code
>
> ```
> select system$get_aws_sns_iam_policy('arn:aws:sns:us-west-2:001234567890:s3_mybucket');
>
> +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> | SYSTEM$GET_AWS_SNS_IAM_POLICY('ARN:AWS:SNS:US-WEST-2:001234567890:S3_MYBUCKET')                                                                                                                                                                   |
> +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> | {"Version":"2012-10-17","Statement":[{"Sid":"1","Effect":"Allow","Principal":{"AWS":"arn:aws:iam::123456789001:user/vj4g-a-abcd1234"},"Action":["sns:Subscribe"],"Resource":["arn:aws:sns:us-west-2:001234567890:s3_mybucket"]}]}                 |
> +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> ```
