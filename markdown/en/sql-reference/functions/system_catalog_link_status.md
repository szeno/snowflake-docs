Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$CATALOG\_LINK\_STATUS

Returns the link status for a specified [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database).

See also:
:   [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database)

## Syntax

Copy code

```
SYSTEM$CATALOG_LINK_STATUS( '<catalog_linked_db_name>' )
```

## Arguments

`'catalog_linked_db_name'`
:   Specifies the name of the catalog-linked database that you want to check the status of.

## Returns

The function returns a JSON object containing the following name/value pairs:

Copy code

```
{
  "executionState":"<value>",
  "failedExecutionStateReason":"<value>",
  "failedExecutionStateErrorCode":"<value>",
  "lastLinkAttemptStartTime":"<value>",
  "failureDetails":[
    {
      "qualifiedEntityName":"<value>",
      "entityDomain":"<value>",
      "operation":"<value>",
      "errorCode":"<value>",
      "errorMessage":"<value>"
    },
    { ... },
    ...
  ]
}
```

Where:

> `executionState`
> :   Current execution state of the linking operation that Snowflake uses to connect to your Iceberg catalog.
>
>     Values:
>
>     - `RUNNING`: The next table discovery sync is scheduled or executing; does not guarantee that all tables have successfully synced.
>     - `FAILED`: The linking operation encountered an error and was unsuccessful.
>
>       If the linking operation fails, resolve the error first. Snowflake then automatically schedules the next table discovery sync, unless
>       discovery has been suspended for the catalog-linked database. If you suspended discovery, run
>       [ALTER DATABASE … RESUME DISCOVERY](/sql-reference/sql/alter-database-catalog-linked) after you resolve the error to resume discovery.
>
>       For example:
>
>       Copy code
>
>       ```
>       ALTER DATABASE IF EXISTS my_linked_db RESUME DISCOVERY;
>       ```
>
> `failedExecutionStateReason`
> :   Error message associated with a `FAILED` execution state. Doesn’t appear in the function output if the last sync attempt
>     was successful.
>
> `failedExecutionStateErrorCode`
> :   Error code associated with a `FAILED` execution state. Does not appear in the function output if the last sync attempt
>     was successful.
>
> `lastLinkAttemptStartTime`
> :   Timestamp that indicates when Snowflake last started the process of discovering and syncing changes in the remote catalog.
>
> `failureDetails`
> :   An array of objects that provide details about entities (for example, tables) in the remote catalog that Snowflake can’t sync.
>     Each object has the following fields:
>
>     `qualifiedEntityName`
>     :   The qualified name of the entity in the remote catalog, relative to the catalog name.
>
>         For example, `namespace_level_1.namespace_level_2.table_name`.
>
>         Type: String
>
>     `entityDomain`
>     :   The entity domain in the remote catalog; for example, TABLE.
>
>         Type: String
>
>     `operation`
>     :   The operation in Snowflake associated with the sync; for example, `CREATE` a table or schema, `DROP`.
>
>         - If the operation is `CATALOG_CONNECTION`, there was an error when Snowflake attempted to connect to the remote catalog.
>         - If the operation is `DISCOVERY`, there was an error when Snowflake attempted to discover the tables or namespaces in your remote
>           catalog. To see which table or namespace caused the error, see `entityDomain`, which will either be `TABLE` or `NAMESPACE`.
>
>         Type: String
>
>     `errorCode`
>     :   Error code associated with the failure.
>
>         Type: String
>
>     `errorMessage`
>     :   Error code associated with the failure.
>
>         Type: String

## Access control requirements

A [role](http://docs.snowflake.com/user-guide/security-access-control-overview#roles) used to execute this SQL command must have either of the following
[privileges](http://docs.snowflake.com/user-guide/security-access-control-overview#privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| OWNERSHIP | The target catalog-linked database. |
| MONITOR | The target catalog-linked database. |

Expand

Show lessSee more

## Usage notes

- The `failureDetails` field returns information about DROP SCHEMA and DROP ICEBERG TABLE failures.
- Returns results as long as you use a role with a privilege on the specified catalog-linked database.
  For more information, see [Database privileges](/user-guide/security-access-control-privileges#label-database-privileges).

## Examples

Retrieve the link status for a catalog-linked database named `my_cld`:

Copy code

```
SELECT SYSTEM$CATALOG_LINK_STATUS('my_cld');
```

Output:

```
{
  "executionState": "RUNNING",
  "lastLinkAttemptStartTime": "2025-02-14T01:35:01.71Z",
  "failureDetails": [
    {
      "qualifiedEntityName": "my_namespace.table_1",
      "entityDomain": "TABLE",
      "operation": "CREATE",
      "errorCode": "0040000",
      "errorMessage": "An internal error occurred. Please contact Snowflake support."
    },
    {
      "qualifiedEntityName": "my_namespace.table_2",
      "entityDomain": "TABLE",
      "operation": "CREATE",
      "errorCode": "0040000",
      "errorMessage": "An internal error occurred. Please contact Snowflake support."
    }
  ]
}
```
