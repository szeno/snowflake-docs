Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$GET\_STAGE\_PRIVATELINK\_AUTHORIZED\_ENDPOINTS

[Business Critical Feature](/user-guide/intro-editions)

This function requires Business Critical (or higher). To inquire about
upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the list of private connectivity sources that have been authorized to
access the internal stage of the current account through previous calls to
[SYSTEM$AUTHORIZE\_STAGE\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_authorize_stage_privatelink_access). Use
this function to verify which sources are currently authorized.

The exact contents of the returned list depend on the cloud provider that
hosts your Snowflake account:

- On Microsoft Azure, the function returns the authorized private endpoints
  along with the approval status of each endpoint connection.
- On Google Cloud, the function returns the authorized VPC networks along with
  the IP CIDR ranges that are allowed to reach the internal stage through each
  VPC network.

See also:
:   [SYSTEM$AUTHORIZE\_STAGE\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_authorize_stage_privatelink_access),
    [SYSTEM$REVOKE\_STAGE\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_revoke_stage_privatelink_access)

## Syntax

Copy code

```
SYSTEM$GET_STAGE_PRIVATELINK_AUTHORIZED_ENDPOINTS()
```

## Arguments

None

## Returns

Returns a JSON-formatted string containing a list of objects. The fields in
each object depend on the cloud provider. If no sources are authorized for the
current account, the function returns an empty list (`[]`).

**Azure**

Each object describes one authorized private endpoint connection and contains
the following string fields:

> `connection_name`
> :   The name of the Azure private endpoint connection.
>
> `endpoint_resource_id`
> :   The Azure resource ID of the private endpoint.
>
> `status`
> :   The approval status of the private endpoint connection (for example,
>     `Approved`, `Pending`, or `Rejected`).

**Google Cloud**

Each object describes one authorized VPC network and contains the following
string fields:

> `vpc_network_id`
> :   The fully qualified path of the Google Cloud VPC network that is
>     authorized to reach the internal stage (for example,
>     `projects/<project>/global/networks/<network>`).
>
> `allowed_ip_cidr_ranges`
> :   The IP CIDR ranges within the VPC network that are allowed to access the
>     internal stage. Currently, every entry returns `0.0.0.0/0`.
>
>     On Google Cloud, `0.0.0.0/0` does not mean that traffic from any source
>     on the public internet is allowed. The function only returns VPC networks
>     that have been explicitly authorized through
>     [SYSTEM$AUTHORIZE\_STAGE\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_authorize_stage_privatelink_access),
>     so `0.0.0.0/0` here means that all traffic originating from within the
>     authorized VPC network is allowed to reach the internal stage.

## Usage notes

- Only account administrators (that is, users with the ACCOUNTADMIN role) can
  call this function.
- This function is supported on Microsoft Azure and Google Cloud. It is not
  supported on Amazon Web Services (AWS) because, on AWS, private connectivity
  to internal stages is established through a VPC endpoint to the entire
  Amazon S3 service in the region rather than to an individual storage
  account or bucket. As a result, no per-account list of authorized
  private connectivity sources is available to return. For more information about how
  internal stage private connectivity works on AWS, see
  [AWS VPC interface endpoints for internal stages](/user-guide/private-internal-stages-aws).

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Examples

The same statement is used on both Azure and Google Cloud; the format of the
returned JSON depends on which cloud provider hosts the account.

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$GET_STAGE_PRIVATELINK_AUTHORIZED_ENDPOINTS();
```

Sample output (the actual return value is a single-line JSON string; the
examples below are pretty-printed for readability).

**Azure**

Copy code

```
[
  {
    "connection_name": "<storage_account>.4d008fc9-9c62-42fd-b5d7-f7f1786654df",
    "endpoint_resource_id": "/subscriptions/<sub_id>/resourceGroups/<rg>/providers/Microsoft.Network/privateEndpoints/test-pe",
    "status": "Approved"
  }
]
```

**Google Cloud**

Copy code

```
[
  {
    "allowed_ip_cidr_ranges": "0.0.0.0/0",
    "vpc_network_id": "projects/<project>/global/networks/<network_1>"
  },
  {
    "allowed_ip_cidr_ranges": "0.0.0.0/0",
    "vpc_network_id": "projects/<project>/global/networks/<network_2>"
  }
]
```

To inspect the individual fields, flatten the JSON result. For example, on
Azure:

Copy code

```
SELECT
  value:connection_name::string      AS connection_name,
  value:endpoint_resource_id::string AS endpoint_resource_id,
  value:status::string               AS status
FROM TABLE(
  FLATTEN(
    input => PARSE_JSON(
      SYSTEM$GET_STAGE_PRIVATELINK_AUTHORIZED_ENDPOINTS()
    )
  )
);
```

On Google Cloud:

Copy code

```
SELECT
  value:vpc_network_id::string AS vpc_network_id
FROM TABLE(
  FLATTEN(
    input => PARSE_JSON(
      SYSTEM$GET_STAGE_PRIVATELINK_AUTHORIZED_ENDPOINTS()
    )
  )
);
```
