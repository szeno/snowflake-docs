Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$EXPORT\_TDS\_FROM\_SEMANTIC\_VIEW

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns a [semantic view](/user-guide/views-semantic/overview) in Tableau Data Source (TDS) format.

## Syntax

Copy code

```
SYSTEM$EXPORT_TDS_FROM_SEMANTIC_VIEW( '<semantic_view_name>' )
```

## Arguments

`'semantic_view_name'`
:   Name of the semantic view to export.

    If the semantic view is not in the current schema and database, specify the
    [fully-qualified name of the view](/sql-reference/name-resolution) (for example, `my_db.my_schema.my_semantic_view`).

## Returns

Returns a VARCHAR value containing the semantic view in TDS format.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any | Semantic view |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

For details about the conversion process and limitations with the conversion, see [Exporting a semantic view to a Tableau Data Source (TDS) file](/user-guide/views-semantic/sql#label-semantic-views-export-tableau).

## Examples

The following statement returns the semantic view `my_sv` in TDS format:

Copy code

```
SELECT SYSTEM$EXPORT_TDS_FROM_SEMANTIC_VIEW('my_sv');
```

```
+------------------------------------------------------------------------+
| SYSTEM$EXPORT_TDS_FROM_SEMANTIC_VIEW('MY_SV')                          |
|------------------------------------------------------------------------|
| <?xml version="1.0" encoding="UTF-8"?>                                 |
| <!--Tableau compatibility notice:                                      |
| ... -->                                                                |
| <datasource xmlns:user="http://www.tableausoftware.com/xml/user" ... > |
| ...                                                                    |
+------------------------------------------------------------------------+
```
