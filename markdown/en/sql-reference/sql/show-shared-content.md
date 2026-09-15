# SHOW SHARED CONTENT IN APPLICATION PACKAGE

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

Shows all of the objects for which you have access privileges that have been shared from a Declarative Native App application package.

## Syntax

Copy code

```
SHOW SHARED CONTENT IN APPLICATION PACKAGE <pkg_name> FOR VERSION <version_name>
```

## Parameters

`pkg_name`
:   Specifies the package (`pkg_name`) containing the shared objects.

`FOR VERSION version_name`
:   Specifies the version (`version_name`) of the package containing the shared objects.

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `version_name` | The automatically generated version name for the shared object. If the object is part of the live version, the value is `LIVE`. |
| `database_name` | The name of the database containing the shared object. |
| `schema_name` | The name of the schema containing the shared object. |
| `entity_name` | The name of the shared object. |
| `entity_type` | The type of the shared object, for example, TABLE, VIEW, or NOTEBOOK. |

Expand

Show lessSee more

## Access control requirements

This command requires a role with the relevant privilege on the entities returned. For example, if the application package contains a shared table, the role must have the USAGE privilege on the database and schema containing the table, and the SELECT privilege on the table.

## Examples

The following example shows how to use the SHOW SHARED CONTENT IN APPLICATION PACKAGE command to list all of the objects in a specific version of a Declarative Native App application package.

Copy code

```
SHOW SHARED CONTENT IN APPLICATION PACKAGE decl_share_app_pkg FOR VERSION VERSION$2;
```

```
+-------------------------------------------------------------------------------+
| version_name | database_name | schema_name     | entity_name    | entity_type |
|--------------+---------------+-----------------+----------------+-------------|
| VERSION$2    | DB_TO_SHARE   | SCHEMA_TO_SHARE | TABLE_TO_SHARE | TABLE       |
+-------------------------------------------------------------------------------+
```
