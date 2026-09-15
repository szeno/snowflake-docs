Categories:
:   [Table functions](/sql-reference/functions-table)

# GET\_CONTACTS

Returns the [contacts](/user-guide/contacts-using) associated with an object.

## Syntax

Copy code

```
SNOWFLAKE.CORE.GET_CONTACTS (
  '<object_name>',
  '<object_type>'
  [ , '<contact_name>' ]
)
```

## Required arguments

`'object_name'`
:   Name of an object that can have contacts associated with it.

`'object_type'`
:   Type of the specified object. Possible values are DATABASE, SCHEMA, and TABLE (for all table-like objects contained in a database and
    schema).

    For a list of supported object types, see [Supported objects](/user-guide/contacts-using#label-contacts-supported-objects).

## Optional arguments

`'contact_name'`
:   Name of a contact. If a contact is specified, the function doesn’t return information about other contacts that are associated with the
    specified object.

## Output

Returns a table, where each row has the following columns:

**Title**

| Column | Data type | Description |
| --- | --- | --- |
| `purpose` | VARCHAR | Describes the relationship between the contact and the specified object. The purpose helps you distinguish between contacts associated with the object so you can reach the right person for assistance. For example, an ACCESS\_APPROVAL purpose indicates that the contact can help you get access to the object. |
| `email_distribution_list` | VARCHAR | Email addresses that can be used to contact someone about the object. |
| `url` | VARCHAR | A URL that can be used to contact someone about the object. |
| `user` | VARCHAR | User who can be contacted about the object. |
| `level` | VARCHAR | Type of object with which the contact was associated. You can use the level to determine where within the object hierarchy the contact was associated. Possible values include DATABASE, SCHEMA, and TABLE (for all table-like objects contained in a database and schema). |

Expand

Show lessSee more

Note

The name of the contact object is intentionally omitted from the output of this function.

## Access control requirements

You must have the CORE\_VIEWER database role to call this function.

## Usage notes

If a contact object includes a list of users, this function returns a separate row for each user in the list.

## Examples

Return a row for each contact associated with the table `t1`.

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.CORE.GET_CONTACTS('t1', 'TABLE'));
```
