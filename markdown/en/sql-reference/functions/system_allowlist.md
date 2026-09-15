Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$ALLOWLIST

Returns host names and port numbers to add to your firewall’s allowed list so that you can access Snowflake from behind your firewall.
The output of this function can then be passed into [SnowCD](/user-guide/snowcd).

Typically, Snowflake customers use a firewall to prevent unauthorized access. By default, your firewall might block access to Snowflake. To
update your firewall’s allowed list, you need to know the host names and port numbers for the URL for your
[Snowflake account](/user-guide/admin-account-identifier), stages, and other hosts used by Snowflake.

For more details about the allowed listing for the Snowflake clients you use, see [Allowing Host names](/user-guide/hostname-allowlist).

## Syntax

Copy code

```
SYSTEM$ALLOWLIST()
```

## Arguments

None.

## Returns

The data type of the returned value is VARIANT. The value is an array of JSON structures. Each JSON structure contains three
key/value pairs:

`type`
:   Snowflake supports the following types:

    `SNOWFLAKE_DEPLOYMENT`
    :   Host name and port number information for your Snowflake account.

    `SNOWFLAKE_DEPLOYMENT_REGIONLESS`
    :   Host name and port number information for your [organization](/user-guide/organizations).

        For more information, see [Account identifiers](/user-guide/admin-account-identifier).

    `STAGE`
    :   Location (such as Amazon S3, Google Cloud Storage, or Microsoft Azure) where files that the Snowflake client can read or write are stored.

    `SNOWSQL_REPO`
    :   Endpoint accessed by SnowSQL to perform automatic downloads or upgrades.

    `OUT_OF_BAND_TELEMETRY`
    :   The hosts to which drivers report metrics and out-of-band incidents such as OCSP issues.

    `CLIENT_FAILOVER`
    :   Host name and port number for the connection URL for [Client Redirect](/user-guide/client-redirect). Note that each row in the query
        output that specifies this value refers to either the primary connection or the secondary connection depending on how the connection
        URLs were configured.

    `CRL_DISTRIBUTION_POINT`
    :   Host name and port number for certificate revocation list (CRL) distribution endpoints.

    `OCSP_CACHE`
    :   Snowflake-provided alternative source of OCSP certificate information in case the primary OCSP responder cannot be reached. Most of the
        latest versions of the Snowflake clients access the OCSP cache rather than connecting directly to the OCSP responder.

    `OCSP_CACHE_REGIONLESS`
    :   Snowflake-provided alternative source of OCSP certificate information for your [organization](/user-guide/organizations). Most of
        the latest versions of the Snowflake clients access the OCSP cache rather than connecting directly to the OCSP responder.

    `OCSP_CLIENT_FAILOVER`
    :   Snowflake-provided alternative source of OCSP certificate information for [Client Redirect](/user-guide/client-redirect).

    `DUO_SECURITY`
    :   The host name for the Duo Security service that is used with [Multi-factor authentication (MFA)](/user-guide/security-mfa) while authenticating to Snowflake.

    `OCSP_RESPONDER`
    :   Host name to contact to verify that the OCSP TLS certificate has not been revoked.

        Note that this value is not necessary when configuring private connectivity to the Snowflake service ; follow the instructions in the
        corresponding topic to select the OCSP value to add to your allowlist.

    `SNOWSIGHT_DEPLOYMENT_REGIONLESS`
    :   Host name and port number for your [organization](/user-guide/organizations) to access Snowsight.

        For more information, see [Account identifiers](/user-guide/admin-account-identifier) and [Snowsight: The Snowflake web interface](/user-guide/ui-snowsight).

    `SNOWSIGHT_DEPLOYMENT`
    :   Host name and port number to access [Snowsight](/user-guide/ui-snowsight) for your Snowflake account.

`host`
:   Specifies the full host name for `type`, for example: `"xy12345.east-us-2.azure.snowflakecomputing.com"`, `"ocsp.snowflakecomputing.com"`.

`port`
:   Specifies the port number for `type`, for example: `443`, `80`.

## Usage notes

- The output might include multiple entries for certain types (e.g. `STAGE`, `OCSP_RESPONDER`).
- Occasionally, Snowflake cannot resolve the socket connection from the client that calls the function, and the statement that calls the
  function fails with one of the following error messages:

  ```
  SYSTEM$ALLOWLIST: Fail to get SSL context
  SYSTEM$ALLOWLIST: SSLContext init failed
  SYSTEM$ALLOWLIST: Could not find host in OCSP dumping
  SYSTEM$ALLOWLIST: Peer unverified
  SYSTEM$ALLOWLIST: Connection failure
  ```

  Additionally, Snowflake returns an empty list for the OCSP fields in the function output. To troubleshoot, you can wait a few minutes and
  rerun the statement if the network connection is transient. If the issue persists, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Examples

To call the function:

> Copy code
>
> ```
> SELECT SYSTEM$ALLOWLIST();
> ```
>
> Sample output:
>
> Copy code
>
> ```
> [
>   {"type":"SNOWFLAKE_DEPLOYMENT",        "host":"xy12345.snowflakecomputing.com",                 "port":443},
>   {"type":"STAGE",                       "host":"sfc-customer-stage.s3.us-west-2.amazonaws.com",  "port":443},
>   ...
>   {"type":"SNOWSQL_REPO",                "host":"sfc-repo.snowflakecomputing.com",                "port":443},
>   ...
>   {"type":"CRL_DISTRIBUTION_POINT",      "host":"crl.r2m01.amazontrust.com",                       "port":80},
>   ...
>   {"type":"OCSP_CACHE",                  "host":"ocsp.snowflakecomputing.com",                     "port":80},
>   {"type":"OCSP_RESPONDER",              "host":"o.ss2.us",                                        "port":80},
>   ...
>   {"type":"APP_SERVICE_PUBLIC_WILDCARD", "host":"*.org-acct-name.us-west-2.aws.snowflake.app",     "port":80},
>   ...
> ]
> ```
>
> In this sample output, note the following:
>
> - For readability, whitespace and newline characters have been added. In addition, some entries have been omitted.
> - The region ID (`us-west-2`) in some of the host names indicates the account is in the US West region; however, the region ID
>   is not utilized in the host name for `SNOWFLAKE_DEPLOYMENT`.

To extract the information into tabular output rather than JSON, use the [FLATTEN](/sql-reference/functions/flatten) function in conjunction with the [PARSE\_JSON](/sql-reference/functions/parse_json)
function:

> Copy code
>
> ```
> SELECT t.VALUE:type::VARCHAR as type,
>        t.VALUE:host::VARCHAR as host,
>        t.VALUE:port as port
> FROM TABLE(FLATTEN(input => PARSE_JSON(SYSTEM$ALLOWLIST()))) AS t;
> ```
>
> Sample output:
>
> Copy code
>
> ```
> +-----------------------------+---------------------------------------------------+------+
> | TYPE                        | HOST                                              | PORT |
> |-----------------------------+---------------------------------------------------+------|
> | SNOWFLAKE_DEPLOYMENT.       | xy12345.snowflakecomputing.com                    | 443  |
> | STAGE                       | sfc-customer-stage.s3.us-west-2.amazonaws.com     | 443  |
>   ...
> | SNOWSQL_REPO                | sfc-repo.snowflakecomputing.com                   | 443  |
>   ...
> | CRL_DISTRIBUTION_POINT.     | crl.r2m01.amazontrust.com                         | 80   |
>   ...
> | OCSP_CACHE                  | ocsp.snowflakecomputing.com                       | 80   |
> | OCSP_RESPONDER              | ocsp.sca1b.amazontrust.com                        | 80   |
>   ...
> | APP_SERVICE_PUBLIC_WILDCARD | *.org-acct-name.us-west-2.aws.snowflake.app       | 443  |
>   ...
> +-----------------------------+---------------------------------------------------+------+
> ```
