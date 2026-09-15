# UNDROP STREAMLIT

Restores the most recent version of a dropped Streamlit object.

See also:
:   [CREATE STREAMLIT](/sql-reference/sql/create-streamlit) , [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit) , [DROP STREAMLIT](/sql-reference/sql/drop-streamlit) , [SHOW STREAMLITS](/sql-reference/sql/show-streamlits) , [DESCRIBE STREAMLIT](/sql-reference/sql/desc-streamlit)

## Syntax

Copy code

```
UNDROP STREAMLIT <name>
```

## Parameters

`name`
:   Specifies the identifier for the Streamlit object to restore.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

If your role does not own the objects in the following table, then your role
must have the listed
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) on those objects:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Streamlit object that you restore |  |
| CREATE STREAMLIT | Schema where you restore the Streamlit object |  |
| USAGE | Warehouse used by the Streamlit app |  |
| USAGE | Compute pool used by the Streamlit app | This privilege is only required if your app has a COMPUTE\_POOL. |
| USAGE | External access integrations used by the Streamlit app | This privilege is only required if your app has EXTERNAL\_ACCESS\_INTEGRATIONS. |
| USAGE | Secrets used by the Streamlit app | This privilege is only required if your app has SECRETS. |
| CREATE STAGE | Schema where you restore the Streamlit object | This privilege is only required to undrop Streamlit objects that were created with the legacy ROOT\_LOCATION parameter. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Streamlit object can only be restored to the database and schema that contained the Streamlit object at the time of deletion.
- If a Streamlit with the same name already exists, an error is returned.

- UNDROP relies on the Snowflake [Time Travel](/user-guide/data-time-travel) feature. An object can be restored only if
  the object was deleted within the [Data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period). The default value is 24 hours.

## Example

The following example restores the most recent version of a dropped Streamlit named `hello_streamlit`:

Copy code

```
UNDROP STREAMLIT hello_streamlit;
```
