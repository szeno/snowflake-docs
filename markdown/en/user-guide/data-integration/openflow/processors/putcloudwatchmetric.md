# PutCloudWatchMetric 2025.10.9.21

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

## Bundle

org.apache.nifi | nifi-aws-nar

## Description

Publishes metrics to Amazon CloudWatch. Metric can be either a single value, or a StatisticSet comprised of minimum, maximum, sum and sample count.

## Tags

amazon, aws, cloudwatch, metrics, publish, put

## Input Requirement

REQUIRED

## Supports Sensitive Dynamic Properties

false

## Properties

| Property | Description |
| --- | --- |
| AWS Credentials Provider service | The Controller Service that is used to obtain AWS credentials provider |
| Communications Timeout |  |
| Endpoint Override URL | Endpoint URL to use instead of the AWS default including scheme, host, port, and path. The AWS libraries select an endpoint URL based on the AWS region, but this property overrides the selected endpoint URL, allowing use with other S3-compatible endpoints. |
| Maximum | The maximum value of the sample set. Must be a double |
| Metric Name | The name of the metric |
| Minimum | The minimum value of the sample set. Must be a double |
| Namespace | The namespace for the metric data for CloudWatch |
| Region |  |
| SSL Context Service | Specifies an optional SSL Context Service that, if provided, will be used to create connections |
| Sample Count | The number of samples used for the statistic set. Must be a double |
| Sum | The sum of values for the sample set. Must be a double |
| Timestamp | A point in time expressed as the number of milliseconds since Jan 1, 1970 00:00:00 UTC. If not specified, the default value is set to the time the metric data was received |
| Unit | The unit of the metric. (e.g Seconds, Bytes, Megabytes, Percent, Count, Kilobytes/Second, Terabits/Second, Count/Second) For details see <http://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html> |
| Value | The value for the metric. Must be a double |
| proxy-configuration-service | Specifies the Proxy Configuration Controller Service to proxy network requests. |

Expand

Show lessSee more

## Relationships

| Name | Description |
| --- | --- |
| failure | FlowFiles are routed to failure relationship |
| success | FlowFiles are routed to success relationship |

Expand

Show lessSee more
