Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_SNOWFLAKE\_PLATFORM\_INFO

Returns platform information for the cloud provider that hosts your Snowflake account.
The function returns different values, depending on your cloud provider:

- For Amazon Web Services (AWS) and Microsoft Azure,
  the function returns the Amazon Virtual Private Cloud (Amazon VPC) IDs or Azure Virtual Network (VNet) IDs.

  A cloud administrator in your company can specify VPC IDs in trust policies. Doing so allows Snowflake to connect to
  the following resources, and denies requests that originate from outside of the virtual network:

  - Your cloud storage.
  - Your [proxy service](/sql-reference/external-functions-introduction#label-external-functions-introduction-miniglossary-proxy-service) for your
    [external function](/sql-reference/external-functions).

  This security restriction can limit traffic to your cloud storage or proxy service on the same cloud platform.
- For Google Cloud, the function returns the project ID and Google Workspace customer ID associated with the Snowflake service account.

  A cloud administrator can use this information to update the domain restriction constraint in an organization policy.

For more information, see the following information for your cloud platform:

AWS:
:   [Allowing the Virtual Private Cloud IDs](/user-guide/data-load-s3-allow)

GCS:
:   [Allow access to Google Cloud Storage](/user-guide/data-load-gcs-allow)

Azure:
:   [Allow the VNet subnet IDs](/user-guide/data-load-azure-allow)

## Syntax

Copy code

```
SYSTEM$GET_SNOWFLAKE_PLATFORM_INFO()
```

## Arguments

None.

## Usage notes

Only returns results for account administrators (users with the ACCOUNTADMIN role).

## Examples

Query the IDs of the virtual network in which your Snowflake account is located:

> Copy code
>
> ```
> SELECT SYSTEM$GET_SNOWFLAKE_PLATFORM_INFO();
> ```
