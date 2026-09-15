# Step 2: Create the proxy service (Amazon API Gateway) in the AWS Management Console

Snowflake does not send data (HTTP POST requests) directly to a remote service. Instead, Snowflake sends the data to a proxy
service that relays the data to the remote service (e.g. an AWS Lambda Function) and back again.

This topic provides instructions for creating and configuring an Amazon API Gateway for use as the proxy service for your
external function.

Configuring an Amazon API Gateway as the proxy service requires several steps, including:

- Creating a new IAM (identity and access management) role in your AWS account.
- Creating an Amazon API Gateway endpoint and configuring it.
- Securing your Amazon API Gateway endpoint.
- Creating an API Integration object in Snowflake.
- Setting up a trust relationship between Snowflake and the new IAM role.

The steps to create these are interleaved because:

- The API integration needs information from the API Gateway, such as the role’s ARN (Amazon Resource Name).
- The API Gateway needs information from the API integration, such as the API\_AWS\_EXTERNAL\_ID and API\_AWS\_IAM\_USER\_ARN.

## Previous step

[Step 1: Create the remote service (AWS Lambda function) in the Management Console](/sql-reference/external-functions-creating-aws-ui-remote-service)

## Create a new IAM role in your AWS account

For Snowflake to authenticate to your AWS account, a Snowflake-owned IAM (identity and access management) user must be
granted permission to assume an IAM role in your AWS account.

The steps to create an IAM role are:

1. Create a new IAM role: In the AWS console, search for IAM, click **Roles**, and then click **Create Role**.
2. When asked to select the type of trusted entity, choose **Another AWS account**.
3. When asked to **Specify accounts that can use this role**, paste the value from the worksheet field named
   `Your AWS Account ID`.

   (Use your AWS Account ID, not Snowflake’s. Snowflake’s ARN will be associated with this IAM role later.)
4. Click **Next: Permissions**.
5. Optionally, set permissions (**Attach permissions policies**).
6. Click **Next: Tags**.
7. Optionally, add tags.
8. Click **Next: Review**.
9. Enter a role name.

   - Record the role name in the `New IAM Role Name` field in the worksheet.
10. Click on the **Create role** button. After you create the role:

- Record the **Role ARN** in the `New IAM Role ARN` field in the worksheet.

## Create the API Gateway endpoint

Before you create and configure your API Gateway, choose whether to use a regional endpoint or a
private endpoint. For more information, see [Choosing your endpoint type: Regional endpoint vs. Private endpoint](/sql-reference/external-functions-creating-aws-planning#label-external-functions-aws-endpoint-type).

If you plan to use a private endpoint, you need the VPC (Virtual Private Cloud) ID that you recorded in the tracking worksheet.

The steps to create an API Gateway endpoint are below:

1. In the AWS management console, select **API Gateway**.
2. Select **Create API**.
3. Select the type of endpoint (regional or private).

   - If you want a regional endpoint, then:

     - Find **REST API** and click on its **Build** button.
   - If you want a private endpoint, then:

     - Find **REST API private** and click on its **Build** button.

   Important

   Make sure that you choose **REST API** or **REST API private**. Do not select **HTTP API**
   or another option.
4. Select the **New API** option.
5. Enter a name for the new API.

   Record this name in the `New API Name` field in the worksheet.
6. If asked to select an **Endpoint Type**, select either **Regional** or **Private**.
7. Leave the `VPC Endpoint IDs` field blank.
8. Click on the **Create API** button.
9. To create a resource, click **Actions**, and then click **Create Resource**.

   Record the resource name in the `API Gateway Resource Name` field of the worksheet.

   Click the **Create Resource** button. The screen displays
   **No methods defined for the resource.**
10. To create a new method, click **Actions** and select **Create Method**.

In the small drop-down menu box under the resource name, select **POST** and then click the grey checkmark beside it.

11. The **Integration type** should be **Lambda Function**. If that is not already selected, then select it.
12. Select the checkbox **Use Lambda Proxy integration**.

It is important to select Lambda proxy integration because
the JSON without Lambda proxy integration would be different from the JSON with Lambda proxy integration.
For more information about Lambda proxy integration, see the AWS documentation for:

- [Lambda integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started-with-lambda-integration.html)
- [API development](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html)

13. In the **Lambda Function** field, paste the `Lambda Function Name` that you recorded in the worksheet.
14. Click on the **Save** button.
15. Click on the **Actions** button, and select the **Deploy API** action.
16. Select or create a stage. Click **Deploy**.
17. Underneath the resource name, you should see **POST**.

If you do not see this, you might need to expand the resource tree by clicking on the triangle that is to the
left of the resource name.

18. Click on **POST**, and then record the **Invoke URL** for the POST request in the
    `Resource Invocation URL` field in the worksheet.

Make sure that the invocation URL includes the name of the resource that you created; if it doesn’t, you might
have clicked on the invocation URL for the stage rather than the resource.

19. Click on **Save Changes**.

## Test the API Gateway

Check that the API Gateway can call your Lambda Function.

1. Follow [AWS’s instructions for testing](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-validation-test.html#api-gateway-request-validation-test-in-console) .
2. At the appropriate step in the AWS instructions, paste the following text into the **Request Body**:

   Copy code

   ```
   {
    "data":
        [
            [0, 43, "page"],
            [1, 42, "life, the universe, and everything"]
        ]
   }
   ```

After you execute the test, you should see the **Request, Status, Latency, and Response Body** appear on
the right (you might need to scroll to see it).

If the returned status is 200, your API Gateway invoked the correct Lambda function.

(This verification step skips authentication, and therefore does not uncover issues with permissions.)

## Secure your Amazon API Gateway endpoint

For an overview of securing proxy service endpoints, such as Amazon API Gateway endpoints,
see [Secure the proxy service](/sql-reference/external-functions-security#label-external-functions-secure-the-proxy-service).

To secure an Amazon API Gateway endpoint:

1. At this point, you should be on the screen that displays your API Gateway information, and you should see
   your resource and **POST** method.

   If you are not already there, do the following:

   1. In the AWS Management Console, go to the API Gateway page.
   2. Select your API Gateway.
   3. In the left-hand pane, click on **Resources**.
   4. Click on the **POST** method. (If you don’t see this, expand the resource tree by
      clicking on the triangle to the left of the resource in the **Resources** pane,
      which is usually the second pane from the left.)
2. Copy the **Method Request ARN** from the **Method Request** box to the `Method Request ARN` field in the
   worksheet.
3. Click on the title **Method Request**.
4. Click the edit symbol beside **Authorization** and select `AWS_IAM` to specify that the method request requires AWS\_IAM authorization.

   Click on the small checkmark next to the menu to confirm your choice.
5. To set the resource policy for the API Gateway to specify who is authorized to invoke the gateway endpoint, click on
   **Resource Policy** in the left-hand column of the window for the API.

   - Regional Endpoint:

     Paste the JSON-formatted resource policy template below into the resource policy editor, then replace the
     placeholders with the appropriate values from the worksheet, as described below.

     Copy code

     ```
     {
         "Version": "2012-10-17",
         "Statement":
         [
       {
       "Effect": "Allow",
       "Principal":
           {
           "AWS": "arn:aws:sts::<12-digit-number>:assumed-role/<external_function_role>/snowflake"
           },
       "Action": "execute-api:Invoke",
       "Resource": "<method_request_ARN>"
       }
         ]
     }
     ```

     Replace the following portions of the resource policy:

     - Replace the `<12-digit-number>` with the value in the field `Your AWS Account ID`, which you recorded in the worksheet.
     - Replace the `<external_function_role>` with the role name from the `New IAM Role Name` field in the
       worksheet.
       For example, if your AWS Role Name is:

       Copy code

       ```
       arn:aws:iam::987654321098:role/MyNewIAMRole
       ```

       then the result should be:

       Copy code

       ```
       "AWS": "arn:aws:sts::987654321098:assumed-role/MyNewIAMRole/snowflake"
       ```
     - Replace the `<method_request_ARN>` with the value in the `Method Request ARN` field of the worksheet.
       This is the ARN of the resource’s POST method.

       > Note
       >
       > Setting the Resource to the Method Request ARN specifies that the API Gateway should allow calls to only the
       > specified resource.
       > It is possible to specify a subset of the Method Request ARN as a prefix, which allows multiple resources to
       > be called from the same API Gateway.
       >
       > For example, if the Method Request ARN is:
       >
       > Copy code
       >
       > ```
       > arn:aws:execute-api:us-west-1:123456789012:a1b2c3d4e5/*/POST/MyResource
       > ```
       >
       > then you could specify just the following prefix:
       >
       > Copy code
       >
       > ```
       > arn:aws:execute-api:us-west-1:123456789012:a1b2c3d4e5/*
       > ```
     - U.S. government GovCloud users only:

       - Update the Method Request ARN to use `aws-us-gov`, e.g.:

         Copy code

         ```
         arn:aws-us-gov:execute-api:us-gov-west-1:123456789012:a1b2c3d4e5/*
         ```
       - Make sure that you use a GovCloud region, e.g. `us-gov-west-1`.
   - Private Endpoint:
     Paste the resource policy template below into the resource policy editor, then replace the placeholders
     with the appropriate values from the worksheet, as described below.

     Copy code

     ```
     {
         "Version": "2012-10-17",
         "Statement": [
       {
           "Effect": "Allow",
           "Principal": {
               "AWS": "arn:aws:sts::<12-digit-number>:assumed-role/<external_function_role>/snowflake"
           },
           "Action": "execute-api:Invoke",
           "Resource": "<method_request_ARN>",
           "Condition": {
               "StringEquals": {
                   "aws:sourceVpc": "<VPC_ID>"
               }
           }
       }
         ]
     }
     ```

     Replace the following portions of the resource policy:

     - Replace the **<12-digit-number>**, **<external\_function\_role>** and **<method\_request\_ARN>**
       as described above for a regional endpoint.
     - Replace the **<VPC\_ID>** with the Snowflake VPC ID for your region, which should be recorded in
       the `Snowflake VPC ID` field of the worksheet.
     - U.S. government GovCloud users only:
       - Update the Method Request ARN to use `aws-us-gov`, e.g.:

         Copy code

         ```
         arn:aws-us-gov:execute-api:us-gov-west-1:123456789012:a1b2c3d4e5/*
         ```
       - Make sure that you use a GovCloud region, e.g. `us-gov-west-1`.
6. Click **Save** to save the resource policy.
7. Deploy the updated API. To do this, click the API name in the breadcrumb trail at the top of the page. Click **Actions** and then click **Deploy API**. Select your deployment stage and click **Deploy**.

In the next step, you create a Snowflake API integration object. Do not close your AWS Management Console
window now; you must return to it later.

## Next step

[Step 3: Create the API integration for AWS in Snowflake](/sql-reference/external-functions-creating-aws-common-api-integration)
