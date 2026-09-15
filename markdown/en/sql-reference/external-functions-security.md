# Securing an external function

This topic describes platform-independent details related to securing external functions.

## Access control

### External functions

External functions, like any user-defined functions (UDFs), follow [access control](/user-guide/security-access-control-overview)
rules:

- External functions have an owner.
- The owner must grant callers (other than the owner) appropriate privilege(s) on the function.

However, external functions have some additional privilege requirement(s):

- Because an external function requires an API integration, the author of the external function must be
  granted USAGE privilege on the API integration.

For more information about UDFs and access control, see [Access control privileges](/user-guide/security-access-control-privileges).

### API integrations

#### Privileges and API integrations

An API integration is a database object. To create an API integration, you need ACCOUNTADMIN privileges or
a Snowflake role with the CREATE INTEGRATION privilege. Account administrators can grant and revoke ownership
and usage privileges on each API integration.

#### Using the API\_KEY option in CREATE API INTEGRATION

Some proxy services (API Gateways) require users to provide subscription information (or other product-related information) when calling
the proxy service. The subscription information can be used to authenticate that the user is a paying customer, enforce usage quotas, etc.

Snowflake now supports *API keys*, also called *subscription keys* (Microsoft Azure’s term), which are alphanumeric string values that a
developer can distribute to users who need to provide subscription information.

Users can provide these keys to Snowflake by using the API\_KEY clause of the CREATE API INTEGRATION statement or the ALTER API INTEGRATION
statement. The API\_KEY clause is optional; you can omit it if the service does not need a key.

An API\_KEY is in addition to, not a substitute for, IAM (Identity and Access Management).

API keys are sensitive. They are not displayed in:

- Query history commands.
- DESCRIBE INTEGRATION commands.
- DESCRIBE API INTEGRATION commands.

The developer of the service chooses how to format the key. The key is opaque to Snowflake, and Snowflake does not validate it.

You can read more about API keys on specific platforms by following the links below:

- [AWS API keys](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)
- [Microsoft Azure subscription keys](https://docs.microsoft.com/en-us/azure/api-management/api-management-subscriptions#what-are-subscriptions)

## Secure the proxy service

Unless your external function is intended to be publicly accessible,
Snowflake strongly recommends securing your proxy service endpoints.

Snowflake uses credential-less API integration objects to authenticate to the proxy service endpoint.
Credential-less API integrations separate responsibilities between administrators and
users. An API integration allows an administrator to create a trust policy between Snowflake
and the cloud provider using the cloud provider’s native authentication and authorization mechanism.
When Snowflake connects to the cloud provider, the cloud provider authenticates and authorizes
access through this trust policy. Using a specific API integration, the administrator can also
specify an allowed list of endpoints that the API integration object can access; this restricts which
proxy services and resources Snowflake can use, enabling the administrator to enforce organizational policies for
data egress and ingress.

More detailed instructions for securing specific proxy service endpoints, such as an Amazon API Gateway, are in
the platform-specific instructions.

## Secure the remote service

If you created your own remote service, don’t forget to secure that.

The details depend upon the implementation of the remote service and are outside the scope of this document.

In most cases, the remote service should use HTTPS, not HTTP.

## Additional security information

- Communications between Snowflake and the proxy server are encrypted using HTTPS.

### Platform-specific security information

#### AWS

- For AWS, all Snowflake HTTP requests (going to the API Gateway) are signed using AWS sigv4 authentication.
  For more information, see
  [AWS sig4 authentication](https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-authenticating-requests.html) .
- Restrict access to your API Gateway endpoints by adding a resource policy. For more information, see
  [Secure your Amazon API Gateway endpoint](/sql-reference/external-functions-creating-aws-ui-proxy-service#label-secure-your-proxy-service-endpoint-aws).
- If you use [private endpoints](/sql-reference/external-functions-creating-aws-planning#label-external-functions-aws-endpoint-type), you might want to read about
  [PrivateLink](/user-guide/admin-security-privatelink).
