Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$DESC\_ICEBERG\_ACCESS\_IDENTITY

Returns information about the Snowflake service principal for a specified external cloud provider
in an account.

See also:
:   [Configure replication for Snowflake-managed Apache Iceberg™ tables](/user-guide/tables-iceberg-replication)

## Syntax

Copy code

```
SYSTEM$DESC_ICEBERG_ACCESS_IDENTITY(
  '<cloud_storage_provider>' [ , '<account_name>' ] )
```

## Required arguments

`'cloud_storage_provider'`
:   Specifies the cloud provider to retrieve service principal information for. You can specify one of the following values for this argument:

    - `'S3'`
    - `'GCS'`
    - `'AZURE'`

## Optional arguments

`'account_name'`
:   Optionally specifies the name of the Snowflake account for which you want to retrieve the service principal information. If specified, you
    must use the value in the `account_name` column returned by the [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts) command.

    If not specified, the function returns information for the current account.

## Returns

The function returns a JSON object containing the following name/value pairs:

**S3**

Copy code

```
{
  "STORAGE_PROVIDER":"S3",
  "STORAGE_AWS_IAM_USER_ARN":"<iam_user_arn>"
}
```

Where:

> `STORAGE_PROVIDER`
> :   The cloud storage provider.
>
> `STORAGE_AWS_IAM_USER_ARN`
> :   The ARN for the AWS IAM user that was created automatically for your Snowflake account.

**GCS**

Copy code

```
{
  "STORAGE_PROVIDER":"GCS",
  "STORAGE_GCP_SERVICE_ACCOUNT":"<service_account_identifier>"
}
```

Where:

> `STORAGE_PROVIDER`
> :   The cloud storage provider.
>
> `STORAGE_GCP_SERVICE_ACCOUNT`
> :   The ID for the GCS service account that was created automatically for your Snowflake account.

**AZURE**

Copy code

```
{
  "STORAGE_PROVIDER":"AZURE",
  "AZURE_MULTI_TENANT_APP_NAME":"<client_app_name>",
  "AZURE_CONSENT_URL_TEMPLATE":"https://login.microsoftonline.com/<your_tenant_id>/oauth2/authorize?client_id=..."
}
```

Where:

> `STORAGE_PROVIDER`
> :   The cloud storage provider.
>
> `AZURE_MULTI_TENANT_APP_NAME`
> :   Name of the Snowflake client application created for your Snowflake account.
>
> `AZURE_CONSENT_URL_TEMPLATE`
> :   Template URL to the Microsoft permissions request page. You must replace `your_tenant_id` with the ID for your
>     tenant that the storage location belongs to.
>
>     To find your tenant ID, log into the Azure portal and click **Microsoft Entra ID** » **Properties**.
>     The tenant ID is displayed in the **Tenant ID** field.

## Usage notes

Only returns results for account administrators (users with the ACCOUNTADMIN role).

## Examples

Retrieve the service principal for Azure:

Copy code

```
SELECT SYSTEM$DESC_ICEBERG_ACCESS_IDENTITY('AZURE', 'MY_TARGET_SNOWFLAKE_ACCOUNT');
```
