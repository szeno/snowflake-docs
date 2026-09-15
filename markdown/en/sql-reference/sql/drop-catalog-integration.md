# DROP CATALOG INTEGRATION

Removes a [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) from the account.

See also:
:   [CREATE CATALOG INTEGRATION](/sql-reference/sql/create-catalog-integration) , [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration) , [SHOW CATALOG INTEGRATIONS](/sql-reference/sql/show-catalog-integrations) , [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration)

## Syntax

Copy code

```
DROP CATALOG INTEGRATION [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the catalog integration to drop. If the identifier contains spaces, special characters,
    or mixed-case characters, the entire string must be enclosed in double quotes. Identifiers enclosed
    in double quotes are also case-sensitive (for example, `"My Catalog"`).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Integration (catalog) | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Dropped catalog integrations cannot be recovered; they must be recreated.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

- You can’t drop or replace a catalog integration if one or more Apache Iceberg™ tables
  are associated with the catalog integration.

  To view the tables that depend on a catalog integration,
  you can use the [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) command and
  a query using the [pipe operator](/sql-reference/operators-flow) (`->>`) that filters on
  the `catalog_name` column.

  Note

  The column identifier (`catalog_name`) is case-sensitive.
  Specify the column identifier exactly as it appears in the SHOW ICEBERG TABLES output.

  For example:

  Copy code

  ```
  SHOW ICEBERG TABLES
    ->> SELECT *
          FROM $1
          WHERE "catalog_name" = 'my_catalog_integration_1';
  ```

## Examples

Drop a catalog integration:

> Copy code
>
> ```
> DROP CATALOG INTEGRATION myInt;
> ```

Drop the catalog integration again, but don’t raise an error if the integration doesn’t exist:

> Copy code
>
> ```
> DROP CATALOG INTEGRATION IF EXISTS myInt;
> ```
