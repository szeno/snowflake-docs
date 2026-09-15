# Jul 29, 2026: Multiple host names for private connectivity endpoints on Microsoft Azure

You can now register more than one host name on an existing private connectivity endpoint using the new
SYSTEM$ADD\_PRIVATELINK\_ENDPOINT\_HOSTNAME and SYSTEM$REMOVE\_PRIVATELINK\_ENDPOINT\_HOSTNAME functions. This is useful for services that expose
multiple host names from a single endpoint, such as a Microsoft Fabric workspace, which needs separate host names for the Iceberg REST
catalog and OneLake storage.

These functions are supported for Snowflake accounts hosted on Microsoft Azure.

For more information, see [SYSTEM$ADD\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_add_privatelink_endpoint_hostname) and
[SYSTEM$REMOVE\_PRIVATELINK\_ENDPOINT\_HOSTNAME](/sql-reference/functions/system_remove_privatelink_endpoint_hostname).
