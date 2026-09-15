Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$REVOKE\_PRIVATELINK

Disables private connectivity to the Snowflake service for the current account.

See also:
:   [SYSTEM$AUTHORIZE\_PRIVATELINK](/sql-reference/functions/system_authorize_privatelink) , [SYSTEM$GET\_PRIVATELINK](/sql-reference/functions/system_get_privatelink) ,
    [SYSTEM$GET\_PRIVATELINK\_AUTHORIZED\_ENDPOINTS](/sql-reference/functions/system_get_privatelink_authorized_endpoints)

## Syntax

**AWS:**

> Copy code
>
> ```
> SYSTEM$REVOKE_PRIVATELINK( '<aws_id>' , '<federated_token>' )
> ```

**Azure:**

> Copy code
>
> ```
> SYSTEM$REVOKE_PRIVATELINK( '<private-endpoint-resource-id>' , '<federated_token>' )
> ```

**GCP**

> Copy code
>
> ```
> SYSTEM$REVOKE_PRIVATELINK( '<gcp_project_id>' , '<access_token>' )
> ```

## Arguments

`'aws_id'`
:   The 12-digit identifier that uniquely identifies your Amazon Web Services (AWS) account, as a string.

`'private-endpoint-resource-id'`
:   The identifier that uniquely identifies the private endpoint in Microsoft Azure (Azure) as a string.

`'federated_token'`
:   The federated token value that contains access credentials for a federated user as a string.

    To obtain this value, execute the appropriate command for the cloud platform that hosts your Snowflake account. Use the command-line tool
    provided by the platform:

    - For Snowflake on AWS:

      Copy code

      ```
      aws sts get-federation-token --name sam
      ```
    - For Snowflake on Azure:

      Copy code

      ```
      az account get-access-token --subscription <SubscriptionID>
      ```

      Where:

      - `SubscriptionID`
        :   The unique identifier for your subscription. For example:

            `13c...`

            To obtain this value, execute the following Azure CLI command in your command-line environment:

            Copy code

            ```
            az account list --output table
            ```

            Note the output value in the `SubscriptionID` column, which is truncated in this example:

            ```
            Name     CloudName   SubscriptionId                        State    IsDefault
            -------  ----------  ------------------------------------  -------  ----------
            MyCloud  AzureCloud  13c...                                Enabled  True
            ```

`'gcp_project_id'`
:   The identifier that uniquely identifies your Google Cloud (GCP) project, as a string.

`'access_token'`
:   The access token value that contains access credentials for a Google Cloud user as a string.

## Usage notes

- Only account administrators (i.e. users with the ACCOUNTADMIN role) can execute this function.
- This function can be used with Snowflake accounts on AWS or Azure; Google Cloud Platform (GCP) is not currently supported.
- Call the [SYSTEM$GET\_PRIVATELINK](/sql-reference/functions/system_get_privatelink) function to verify whether your Snowflake account is authorized
  to use private connectivity to the Snowflake service.
- Call the [SYSTEM$AUTHORIZE\_PRIVATELINK](/sql-reference/functions/system_authorize_privatelink) function to enable your Snowflake account to use private
  connectivity to the Snowflake service.

## Examples

Disable AWS PrivateLink for your Snowflake account on AWS. Note that the values are truncated in this example.

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> select SYSTEM$REVOKE_PRIVATELINK(
>     '185...',
>     '{
>       "Credentials": {
>           "AccessKeyId": "ASI...",
>           "SecretAccessKey": "enw...",
>           "SessionToken": "Fwo...",
>           "Expiration": "2021-01-07T19:06:23+00:00"
>       },
>       "FederatedUser": {
>           "FederatedUserId": "185...:sam",
>           "Arn": "arn:aws:sts::185...:federated-user/sam"
>       },
>       "PackedPolicySize": 0
>   }'
>   );
> ```

Disable Azure Private Link for your Snowflake account on Azure. Note that the values are truncated in this example.

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> select SYSTEM$REVOKE_PRIVATELINK(
>   '/subscriptions/26d.../resourcegroups/sf-1/providers/microsoft.network/privateendpoints/test-self-service',
>   'eyJ...');
> ```

Disable Google Cloud Private Service Connect for your Snowflake account on GCP:

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> select SYSTEM$REVOKE_PRIVATELINK(
>   'my-gcp-project-id',
>   'ya29.a0AcM612zT4pJaXdYfwgY8aiMoDE9W_xkqQ20coFTB1TJcImKDPo...'
>   );
> ```
