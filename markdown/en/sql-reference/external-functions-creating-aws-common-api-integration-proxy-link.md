# Step 4: Link the API integration for AWS to the proxy service in the Management Console

This topic provides instructions for linking the API integration object in Snowflake to your proxy service (i.e.
Amazon API Gateway). You do this by creating a trust relationship between Snowflake and the IAM (identity and access
management) role you created earlier.

The instructions are the same regardless of whether you are using the Management Console or the
CloudFormation template.

## Previous step

[Step 3: Create the API integration for AWS in Snowflake](/sql-reference/external-functions-creating-aws-common-api-integration)

## Set up the trust relationship(s) between Snowflake and the new IAM role

In the AWS Management Console:

1. Select **IAM**.
2. Select **Roles**.
3. In the worksheet, look up the value in the `New IAM Role Name` field, then
   look for the same value (role name) in the AWS Management Console.
4. Click on the **Trust relationships** tab, then click on the button **Edit trust relationship**.

   This should open the **Policy Document** into which you can add authentication information.
5. In the **Policy Document**, find the **Statement.Principal.AWS** field and replace the value (not the
   key) with the value in the `API_AWS_IAM_USER_ARN` field of the worksheet.
6. Find the **Statement.Condition** field. Initially, this should contain only curly braces (“{}”).
7. Paste the following between the curly braces:
   `"StringEquals": { "sts:ExternalId": "xxx" }`
8. Replace the `xxx` with the value for the `API_AWS_EXTERNAL_ID` field in the worksheet.
9. After you are done editing the **Policy Document** for the trust relationship, it should look similar to the
   following:

   Copy code

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::1234567898012:user/development/development_user"
      },
      "Action": "sts:AssumeRole",
      "Condition": {"StringEquals": { "sts:ExternalId": "EXTERNAL_FUNCTIONS_SFCRole=3_8Hcmbi9halFOkt+MdilPi7rdgOv=" }}
    }
     ]
   }
   ```
10. Click on **Update Trust Policy**.

## Next step

[Step 5: Create the external function for AWS in Snowflake](/sql-reference/external-functions-creating-aws-common-ext-function)
