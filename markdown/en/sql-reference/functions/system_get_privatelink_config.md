Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_PRIVATELINK\_CONFIG

Returns a JSON representation of the Snowflake account information necessary to facilitate the self-service configuration of private
connectivity to the Snowflake service or Snowflake internal stages.

## Syntax

Copy code

```
SYSTEM$GET_PRIVATELINK_CONFIG()
```

## Arguments

None.

## Returns

The function returns a JSON object containing the following name/value pairs based on the cloud platform where your Snowflake account is
located:

**AWS**

> Copy code
>
> ```
> {
>   "regionless-snowsight-privatelink-url": "<privatelink_org_snowsight_url>",
>   "privatelink-account-name": "<account_identifier>",
>   "privatelink-connection-ocsp-urls": "<client_redirect_ocsp_url_list>",
>   "snowsight-privatelink-url": "<privatelink_region_snowsight_url>",
>   "privatelink-internal-stage": "<privatelink_stage_endpoint>",
>   "privatelink-account-url": "<privatelink_account_url>",
>   "privatelink-connection-urls": "<privatelink_connection_url_list>",
>   "regionless-privatelink-account-url": "<privatelink_org_account_url>",
>   "privatelink-ocsp-url": "<privatelink_ocsp_url>",
>   "privatelink-vpce-id": "<aws_vpce_id>",
>   "privatelink-account-principal": "<aws_principal_arn>",
>   "regionless-privatelink-ocsp-url": "<privatelink_org_ocsp_url>",
>   "app-service-privatelink-url": "<privatelink_streamlit_url>",
>   "app-service-privatelink-url-next": "<privatelink_account_scoped_app_url>",
>   "privatelink-dashed-urls-for-duo": "<privatelink_duo_url_list>"
> }
> ```

**Microsoft Azure**

> Copy code
>
> ```
> {
>   "regionless-snowsight-privatelink-url": "<privatelink_org_snowsight_url>",
>   "privatelink-account-name": "<account_identifier>",
>   "privatelink-connection-ocsp-urls": "<client_redirect_ocsp_url_list>",
>   "snowsight-privatelink-url": "<privatelink_region_snowsight_url>",
>   "privatelink-internal-stage": "<privatelink_stage_endpoint>",
>   "privatelink-snowflake-managed-storage-volume-nfs": "<privatelink_volume_nfs_endpoint>",
>   "privatelink-snowflake-managed-storage-volume-fs": "<privatelink_volume_fs_endpoint>",
>   "privatelink-account-url":"<privatelink_account_url>",
>   "privatelink-connection-urls": "<privatelink_connection_url_list>",
>   "regionless-privatelink-account-url": "<privatelink_org_account_url>",
>   "privatelink-ocsp-url": "<privatelink_ocsp_url>",
>   "privatelink-pls-id": "<azure_privatelink_service_id>",
>   "regionless-privatelink-ocsp-url": "<privatelink_org_ocsp_url>",
>   "privatelink-dashed-urls-for-duo": "<privatelink_duo_url_list>"
> }
> ```

**Google Cloud Platform**

> Copy code
>
> ```
> {
>   "regionless-snowsight-privatelink-url": "<privatelink_org_snowsight_url>",
>   "privatelink-account-name": "<account_identifier>",
>   "privatelink-connection-ocsp-urls": "<client_redirect_ocsp_url_list>",
>   "snowsight-privatelink-url": "<privatelink_region_snowsight_url>",
>   "privatelink-account-url": "<privatelink_account_url>",
>   "privatelink-connection-urls": "<privatelink_connection_url_list>",
>   "regionless-privatelink-account-url": "<privatelink_org_account_url>",
>   "privatelink-ocsp-url": "<privatelink_ocsp_url>",
>   "privatelink-gcp-service-attachment": "<snowflake_service_endpoint>",
>   "regionless-privatelink-ocsp-url": "<privatelink_org_ocsp_url>",
>   "privatelink-dashed-urls-for-duo": "<privatelink_duo_url_list>"
> }
> ```

Where:

> `regionless-snowsight-privatelink-url`
> :   The URL for your [organization](/user-guide/organizations) to access Snowsight using private connectivity to the Snowflake
>     service.
>
>     Use this URL to create a canonical name (i.e. CNAME) for DNS resolution. This URL should match the output for the
>     `SNOWSIGHT_DEPLOYMENT_REGIONLESS` (i.e. `TYPE`) from the [SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink)
>     function.
>
>     For more information, see [Account identifiers](/user-guide/admin-account-identifier) and [Snowsight: The Snowflake web interface](/user-guide/ui-snowsight).
>
> `privatelink-account-name`
> :   The identifier for your Snowflake account.
>
>     Use this value with clients for [Applications and tools for connecting to Snowflake](/guides-overview-connecting).
>
>     For more information, see [Account identifiers](/user-guide/admin-account-identifier).
>
> `privatelink-connection-ocsp-urls`
> :   The list of OCSP URLs for use with [Redirecting client connections](/user-guide/client-redirect).
>
>     The list of values should match the output for `OCSP_CLIENT_FAILOVER` from the SYSTEM$ALLOWLIST\_PRIVATELINK function.
>
> `snowsight-privatelink-url`
> :   The URL containing the [cloud region](/user-guide/intro-regions) to access Snowsight and the Snowflake Marketplace using
>     private connectivity to the Snowflake service.
>
>     Use this URL to create a canonical name (i.e. CNAME) for DNS resolution. This URL should match the output for the
>     `SNOWSIGHT_DEPLOYMENT` (i.e. `TYPE`) from the [SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink) function.
>
>     For more information, see [Account identifiers](/user-guide/admin-account-identifier) and [Snowsight: The Snowflake web interface](/user-guide/ui-snowsight).
>
> `privatelink-internal-stage`
> :   The endpoint to connect to your Snowflake internal stage using AWS PrivateLink or Azure Private Link.
>
>     Use this value with private connectivity to Snowflake internal stages.
>
>     The visibility of this key and the corresponding value in the query result depends on the
>     [ENABLE\_INTERNAL\_STAGES\_PRIVATELINK](/sql-reference/parameters#label-enable-internal-stages-privatelink) parameter setting. The default setting for this parameter is `FALSE`. You must set
>     this parameter to `TRUE` prior to executing this system function to obtain the internal stage endpoint in the query result.
>
> `privatelink-snowflake-managed-storage-volume-nfs`
> :   The endpoint to connect to your non failsafe Snowflake-managed storage volume using Azure Private Link.
>
>     Use this value with private connectivity to Snowflake-managed storage volumes for Apache Iceberg tables.
>
>     The visibility of this key and the corresponding value in the query result depends on the
>     [ENABLE\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PRIVATELINK](/sql-reference/parameters#label-enable-snowflake-managed-storage-volume-privatelink) parameter setting. The default setting for this parameter is
>     `FALSE`. You must set this parameter to `TRUE` prior to executing this system function to obtain the endpoint in the query
>     result.
>
> `privatelink-snowflake-managed-storage-volume-fs`
> :   The endpoint to connect to your failsafe Snowflake-managed storage volume using Azure Private Link.
>
>     Use this value with private connectivity to Snowflake-managed storage volumes for Apache Iceberg tables.
>
>     The visibility of this key and the corresponding value in the query result depends on the
>     [ENABLE\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PRIVATELINK](/sql-reference/parameters#label-enable-snowflake-managed-storage-volume-privatelink) parameter setting. The default setting for this parameter is
>     `FALSE`. You must set this parameter to `TRUE` prior to executing this system function to obtain the endpoint in the query
>     result.
>
> `privatelink-account-url`
> :   The URL to connect to your Snowflake account using AWS PrivateLink, Azure Private Link, or Google Cloud Private Service Connect.
>
>     Use this value to create a canonical name (i.e. CNAME) for DNS resolution. This URL should match the output from
>     [SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink).
>
>     For more information on URL formats, see [Account identifiers](/user-guide/admin-account-identifier).
>
> `privatelink-connection-urls`
> :   The list of connection URLs for [Client Redirect](/user-guide/client-redirect).
>
>     Use these URLs to create a canonical name (i.e. CNAME) for DNS resolution. These URL should match the output for
>     `CLIENT_FAILOVER` (i.e. `TYPE`) from the [SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink) function.
>
> `regionless-privatelink-account-url`
> :   The private connectivity URL that includes your organization name and account name.
>
>     This value matches the output value of `SNOWFLAKE_DEPLOYMENT_REGIONLESS` in the
>     [SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink) function.
>
> `privatelink-ocsp-url`
> :   The OCSP URL corresponding to your Snowflake account identifier that uses AWS PrivateLink, Microsoft Azure Private Link, or Google
>     Cloud Private Service Connect.
>
>     Use this value to create a canonical name (i.e. CNAME) for DNS resolution.
>
> `privatelink-vpce-id`
> :   The AWS VPCE ID for your account identifier.
>
>     Use this value to create an AWS VPC endpoint (i.e. VPCE).
>
> `privatelink-account-principal`
> :   The AWS principal ARN to allow for outbound private connections to your VPC endpoint services.
>
>     Use this value to set the
>     [allowed principal](https://docs.aws.amazon.com/vpc/latest/privatelink/configure-endpoint-service.html#add-remove-permissions)
>     of your endpoint service, which allows Snowflake to connect to your endpoint service via
>     [AWS PrivateLink](/user-guide/private-manage-endpoints-aws).
>
> `privatelink-pls-id`
> :   The Microsoft Azure Private Link Service ID for your account identifier in the format of an alias. For example:
>
>     > `sf-pvlinksvc-azurecentralus.<unique_identifier>.centralus.azure.privatelinkservice`
>     >
>     > Where the `<unique_identifier>` is in GUID/UUID format.
>
>     Use this value to create an Azure Private Link private endpoint. If you receive an error while creating the private endpoint, contact
>     [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) and ask for the resource ID that is associated with this alias value.
>
> `privatelink-gcp-service-attachment`
> :   The endpoint for the Snowflake service when using Google Cloud Private Service Connect.
>
>     Use this value when creating a forwarding rule to route the Private Service Connect endpoint in your VPC to the Snowflake service.
>
> `"regionless-privatelink-ocsp-url`
> :   The OCSP URL for your [account identifier](/user-guide/admin-account-identifier).
>
>     The value is recorded as follows:
>
>     `"ocsp.org_name-account_name.privatelink.snowflakecomputing.com"`
>
>     Where:
>
>     - `org_name` is the name of your Snowflake organization.
>     - `account_name` is the unique name of your account within your organization.
>
> `app-service-privatelink-url`
> :   The PrivateLink endpoint URL used to route traffic to Snowflake-hosted app services, such as Streamlit or Notebooks.
>
> `app-service-privatelink-url-next`
> :   The per-account PrivateLink endpoint URL used to route traffic to Snowflake-hosted app services, such as
>     Streamlit, Notebooks, and Snowpark Container Services. This key is returned when account-scoped private link URLs
>     are not enabled for your account.
>
>     You can enable account-scoped private link URLs by setting the
>     [ENABLE\_PER\_ACCOUNT\_APP\_SERVICE\_PRIVATELINK\_URL](/sql-reference/parameters#label-enable-per-account-app-service-privatelink-url)
>     account parameter to `TRUE`.
>
> `privatelink-dashed-urls-for-duo`
> :   The list of dashed variant URLs is shown only when the hostname contains an underscore. These URLs are used for Duo Multi-Factor Authentication.

## Usage notes

- Only account administrators (i.e. users with the ACCOUNTADMIN role) can execute this function.
- For Snowflake accounts on Microsoft Azure, if you call the function and the query time is greater than one minute, please contact
  [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Examples

Retrieve the JSON information for your Snowflake account on AWS:

> Copy code
>
> ```
> SELECT SYSTEM$GET_PRIVATELINK_CONFIG();
> ```

You can optionally run the following command to flatten the JSON output. The following output is an example for a Snowflake account on
Microsoft Azure:

> Copy code
>
> ```
> select key, value from table(flatten(input=>parse_json(SYSTEM$GET_PRIVATELINK_CONFIG())));
>
> +--------------------------------------+--------------------------------------+
> | KEY                                  | VALUE                                |
> +--------------------------------------+--------------------------------------+
> | regionless-snowsight-privatelink-url | "<privatelink_org_snowsight_url>"    |
> |--------------------------------------+--------------------------------------|
> | privatelink-account-name             | "<account_identifier>"               |
> |--------------------------------------+--------------------------------------|
> | privatelink-connection-ocsp-urls     | "<client_redirect_ocsp_url_list>"    |
> |--------------------------------------+--------------------------------------|
> | snowsight-privatelink-url            | "<privatelink_region_snowsight_url>" |
> |--------------------------------------+--------------------------------------|
> | privatelink-internal-stage           | "<privatelink_stage_endpoint>"       |
> |--------------------------------------+--------------------------------------|
> | privatelink-snowflake-managed-       | "<privatelink_volume_nfs_endpoint>"  |
> | storage-volume-nfs                   |                                      |
> |--------------------------------------+--------------------------------------|
> | privatelink-snowflake-managed-       | "<privatelink_volume_fs_endpoint>"   |
> | storage-volume-fs                    |                                      |
> |--------------------------------------+--------------------------------------|
> | privatelink-account-url              | "<privatelink_account_url>"          |
> |--------------------------------------+--------------------------------------|
> | privatelink-connection-urls          | "<privatelink_connection_url_list>"  |
> |--------------------------------------+--------------------------------------|
> | privatelink-pls-id                   | "<azure_private_link_service_id>"    |
> |--------------------------------------+--------------------------------------|
> | regionless-privatelink-account-url   | "<privatelink_org_account_url>"      |
> |--------------------------------------+--------------------------------------|
> | privatelink-ocsp-url                 | "<privatelink_ocsp_url>"             |
> |--------------------------------------+--------------------------------------|
> | regionless-privatelink-ocsp-url      | "<privatelink_org_ocsp_url>"         |
> +--------------------------------------+--------------------------------------+
> ```
