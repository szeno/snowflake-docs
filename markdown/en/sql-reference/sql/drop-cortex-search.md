# DROP CORTEX SEARCH SERVICE

Removes the specified [Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) from the current schema.

## Syntax

Copy code

```
DROP CORTEX SEARCH SERVICE <name>;
```

## Parameters

`name`
:   Specifies the identifier for the Cortex Search service to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access Control Requirements

| Privilege | Object |
| --- | --- |
| OWNERSHIP | Cortex Search service you want to remove. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage Notes

## Examples

The following example drops the Cortex Search service named `mysvc`:

Copy code

```
DROP CORTEX SEARCH SERVICE mysvc;
```

```
+------------------------------+
| status                       |
|------------------------------|
| mysvc successfully dropped.  |
+------------------------------+
```
