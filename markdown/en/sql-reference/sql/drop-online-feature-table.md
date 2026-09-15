# DROP ONLINE FEATURE TABLE

Removes the specified [online feature table](/sql-reference/sql/create-online-feature-table) from the current/specified
schema.

See also:
:   [CREATE ONLINE FEATURE TABLE](/sql-reference/sql/create-online-feature-table) , [ALTER ONLINE FEATURE TABLE](/sql-reference/sql/alter-online-feature-table), [DESCRIBE ONLINE FEATURE TABLE](/sql-reference/sql/desc-online-feature-table) , [SHOW ONLINE FEATURE TABLES](/sql-reference/sql/show-online-feature-tables)

## Syntax

Copy code

```
DROP ONLINE FEATURE TABLE [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the online feature table to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`IF EXISTS`
:   Specifies to not return an error if the online feature table does not exist.

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Online feature table | Role that has the OWNERSHIP privilege on the online feature table. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage Notes

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

The following example drops the online feature table named `my_online_feature_table`:

Copy code

```
DROP ONLINE FEATURE TABLE my_online_feature_table;
```

```
+------------------------------------------------+
| status                                         |
|------------------------------------------------|
| MY_ONLINE_FEATURE_TABLE successfully dropped. |
+------------------------------------------------+
```

The following example drops the online feature table named `my_online_feature_table` if it exists:

Copy code

```
DROP ONLINE FEATURE TABLE IF EXISTS my_online_feature_table;
```
