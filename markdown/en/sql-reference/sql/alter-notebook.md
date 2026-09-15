# ALTER NOTEBOOK

Modifies the properties of an existing [notebook](/user-guide/ui-snowsight/notebooks).

## Syntax

Copy code

```
ALTER NOTEBOOK [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER NOTEBOOK [ IF EXISTS ] <name> SET
  [ COMMENT = '<string_literal>' ]
  [ QUERY_WAREHOUSE = <warehouse_to_run_nb_and_sql_queries_in> ]
  [ IDLE_AUTO_SHUTDOWN_TIME_SECONDS = <number_of_seconds> ]
  [ SECRETS = ('<secret_variable_name>' = <secret_name>) [ , ... ] ]
```

## Parameters

`name`
:   Specifies the identifier for the notebook to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Changes the name of the notebook to `new_name`. The new identifier must be unique for the schema.

    For more details about identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When an object is renamed, other objects that reference it must be updated with the new name.

`SET ...`
:   Sets one or more specified properties or parameters for the notebook:

`QUERY_WAREHOUSE = warehouse_name`
:   Specifies the warehouse where SQL queries in the notebook are run.
    This parameter is optional. However, it is required to run the EXECUTE NOTEBOOK command.

`IDLE_AUTO_SHUTDOWN_TIME_SECONDS = number_of_seconds`
:   Number of seconds of idle time before the notebook is shut down automatically. This parameter is available for notebooks running
    on both Warehouse and Container Runtime. The value must be an integer between 60 and 259200 (72 hours).

    Default: 3600 seconds

`SECRETS = '(secret_variable_name' = secret_name [ , ... ])`
:   Sets secret variables for the notebook.

    - `secret_variable_name` - The variable that will be used in the notebook cell when retrieving information from the secret.
    - `secret_name` - The name of the Snowflake secret.

`UNSET ...`
:   Unsets one or more specified properties or parameters for the notebook, which resets the properties to the defaults:

    - QUERY\_WAREHOUSE
    - COMMENT

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE or OWNERSHIP | Notebook | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example renames the notebook named `my_notebook` to `notebook_v2`:

Copy code

```
ALTER NOTEBOOK my_notebook RENAME TO notebook_v2;
```

The following example unsets the QUERY\_WAREHOUSE property:

Copy code

```
ALTER NOTEBOOK my_notebook UNSET QUERY_WAREHOUSE;
```
