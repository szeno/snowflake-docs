# Planning an external function for AWS

This topic helps you prepare to create an external function for AWS (Amazon Web Services) using either the AWS Management Console
or an AWS CloudFormation template provided by Snowflake.

## Prerequisites

These instructions assume that you are an experienced AWS Management Console user.

You need:

- An account with AWS, including privileges to:

  - Create AWS roles via IAM (identity and access management).
  - Create AWS Lambda Functions.
  - Create an API Gateway endpoint.
- A Snowflake account in which you have ACCOUNTADMIN privileges or a role with the CREATE INTEGRATION privilege.
- If you plan to use a private endpoint, you need your Virtual Private Cloud (VPC) ID.
  (You must use a VPC ID, not a VPC Endpoint ID. VPC Endpoint IDs can change over time.)

  If you do not already have your VPC ID, you can find it by executing the following command in the Snowflake web interface:

  Copy code

  ```
  select system$get_snowflake_platform_info();
  ```

  The output will resemble:

  ```
  {
    "snowflake-vpc-id": ["vpc-12345678"],
    "snowflake-egress-vpc-ids": [
   ...
  {
    "id": "vpc-12345678",
    "expires": "2025-03-01T00:00:00",
    "purpose": "generic"
  },
  ...
  ]
   }
  ```

  From the function output, for each property identified with “purpose”: “generic”, record the corresponding VPC ID(s).

  After you decide whether to create your external function by using the AWS Management Console or an
  AWS CloudFormation template, copy the VPC IDs to the appropriate tracking worksheet:

  - [Management Console worksheet](#label-aws-management-console-tracking-worksheet).
  - [CloudFormation template worksheet](#label-aws-cloudformation-template-tracking-worksheet).

## Choosing your endpoint type: Regional endpoint vs. Private endpoint

You access a proxy service (such as Amazon API Gateway) via a URI, often referred to as an *endpoint*.
The instructions for creating your Amazon API Gateway ask you to choose one of the following types of endpoints:

- A regional endpoint.
- A private endpoint.

The following information can help you choose the type of endpoint.

A regional endpoint can be accessed across AWS regions, or even across cloud platforms.
Your Snowflake instance, your proxy service, and your remote service can all be in different regions or even on
different cloud platforms. For example, a Snowflake instance running on Azure could send requests to an Amazon API Gateway
regional endpoint, which in turn could forward data to a remote service running on GCP.

A private endpoint can be configured to allow access only within a region. For example, you can configure a private endpoint
to allow access from only a Snowflake VPC (Virtual Private Cloud) in the same AWS region. Communication between a Snowflake VPC
and a private endpoint uses AWS PrivateLink.

For more details about the types of endpoints on AWS, see:

- [Amazon API Gateway concepts](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-basic-concept.html)
- [Amazon API Gateway endpoint types](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-endpoint-types.html)

If you want to use a private endpoint, and you are not sure which region you are using, you can look up your
region by doing either of the following:

- Call the SQL function `CURRENT_REGION()` (e.g. `SELECT CURRENT_REGION()`).
- Check your Snowflake account hostname, which normally indicates the cloud provider and region. For more
  information about account hostnames, regions, and cloud providers, see [Supported cloud regions](/user-guide/intro-regions).

To use a private endpoint, your account must meet the following requirements:

- Business Critical (or higher) edition of Snowflake.

## Choosing the method for creating the external function

Snowflake provides instructions for two ways to create an external function on AWS:

- AWS Management Console web interface
- AWS CloudFormation template provided by Snowflake

### AWS Management Console

You can use the [AWS Management Console](https://aws.amazon.com/console/) to create a Lambda Function (as the remote service)
and an Amazon API Gateway instance (as the proxy service). If you choose this method, you also use the AWS Management Console to
configure security-related settings.

The instructions for creating an external function using the AWS Management Console include a sample Lambda Function and details
for creating a basic API Gateway:

- First-time users can use the instructions with little or no modification.
- Experienced users can use the instructions and sample Lambda Function as a starting point for creating a custom Lambda Function
  and a custom-configured API Gateway.

### AWS CloudFormation template

The CloudFormation template performs both of the following steps in creating an external function:

- Creating the remote service (an AWS Lambda Function).
- Creating and configuring the proxy service (an Amazon API Gateway).

The template also:

- Creates two IAM roles (one for the Lambda Function and one for the API Gateway).
- Configures a resource policy for the API Gateway.

## Preparing to use the AWS Management Console

### Create a worksheet for tracking required information

As you create your external function, you should record specific information that you enter (e.g. the Resource Invocation URL)
so that you can use that information in subsequent steps. The worksheet below helps you track this information.

Copy code

```
===========================================================================
================ Tracking Worksheet: AWS Management Console ===============
===========================================================================

****** Step 1: Information about the Lambda Function (remote service) *****

Your AWS Account ID: ______________________________________________________

Lambda Function Name: _____________________________________________________

******** Step 2: Information about the API Gateway (proxy Service) ********

New IAM Role Name: ________________________________________________________

New IAM Role ARN: _________________________________________________________

Snowflake VPC ID (optional): ______________________________________________

New API Name: _____________________________________________________________

API Gateway Resource Name: ________________________________________________

Resource Invocation URL: __________________________________________________

Method Request ARN: _______________________________________________________

*** Step 3: Information about the API Integration and External Function ***

API Integration Name: _____________________________________________________

API_AWS_IAM_USER_ARN: _____________________________________________________

API_AWS_EXTERNAL_ID: ______________________________________________________

External Function Name: ___________________________________________________
```

## Preparing to use an AWS CloudFormation template

### Download the template

The template is available for download from the
[deployment templates directory](https://github.com/Snowflake-Labs/sfguide-external-functions-examples/tree/main/DeploymentTemplates/aws/BasicSetup.yaml)
in the Snowflake repository in GitHub.

### Create a worksheet for tracking required information

As you create your external function, you should record specific information that you enter (e.g. the Resource Invocation URL)
so that you can use that information in subsequent steps. The worksheet below helps you track this information.

Copy code

```
===========================================================================
================== Tracking Worksheet: CloudFormation Template ============
===========================================================================

New IAM Role Name: ________________________________________________________

New IAM Role ARN: _________________________________________________________

Resource Invocation URL: __________________________________________________

API_AWS_IAM_USER_ARN: _____________________________________________________

API_AWS_EXTERNAL_ID: ______________________________________________________
```

## Additional resources for building external functions on AWS

When you are ready to create your own remote service for your own external function, you might want to look at the
examples of remote services based on Lambda Functions that are available in
[the Snowflake Labs](https://github.com/Snowflake-Labs/sfguide-external-functions-examples).

## Next step

AWS Management Console:
:   [Step 1: Create the remote service (AWS Lambda function) in the Management Console](/sql-reference/external-functions-creating-aws-ui-remote-service)

AWS CloudFormation template:
:   [Step 1: Use the template to create the remote service (AWS Lambda function) and proxy service (API Gateway)](/sql-reference/external-functions-creating-aws-template-services)
