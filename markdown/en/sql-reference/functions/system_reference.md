Categories:
:   [System functions](/sql-reference/functions-system) (Information)

# SYSTEM$REFERENCE

Returns a [reference](/sql-reference/references) to an object (a table, view, or function). When
you execute SQL actions on a reference to an object, the actions are performed using the role of the user who created the
reference.

Note

As an alternative to calling this function, you can use the TABLE keyword, if you need to create a reference to an object that
you don’t plan to modify (for example, if you are passing in a table that the stored procedure will query) and you want that
reference to be valid for the scope of the call (rather than for the entire session). See
[Using the TABLE keyword to create a reference to a table, view, or query](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-table-keyword).

See also:
:   [SYSTEM$QUERY\_REFERENCE](/sql-reference/functions/system_query_reference)

## Syntax

Copy code

```
SYSTEM$REFERENCE('<object_type>', '<object_identifier>',
  [ , '<reference_scope>' [ , '<privilege>' [ , '<privilege>' ... ] ] ] )
```

## Arguments

**Required**

`'object_type'`
:   Type of the object. You can specify one of the following values:

    - `api_integration`
    - `compute_pool`
    - `cortex_agent`
    - `database`
    - `external_access_integration`
    - `external_table`
    - `external_volume`
    - `function`
    - `materialized_view`
    - `policy`
    - `pipe`
    - `procedure`
    - `row_access_policy`
    - `secret`
    - `schema`
    - `snowflake_intelligence`
    - `table`
    - `tag`
    - `task`
    - `view`
    - `warehouse`

`'object_identifier'`
:   Identifier for the object. If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    For more details about identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

**Optional**

`'reference_scope'`
:   Specifies the scope of the reference.

    If `'CALL'` or omitted, specifies that the reference is valid within the context in which it was created.
    See [Specifying the scope of the reference](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-scope).

    If `'SESSION'`, specifies that the reference should be valid for the duration for the session.

    If `'PERSISTENT'`, specifies that the reference should be valid until the object is dropped. See
    [persistent references](/sql-reference/references#label-persistent-reference).

    Note: If you need to specify the `'privilege'` argument, the `'reference_scope'` argument is required.

    Valid values:

    - `'CALL'`
    - `'SESSION'`
    - `'PERSISTENT'`

    Default value: `'CALL'`

`'privilege'`
:   Additional [privilege](/user-guide/security-access-control-privileges) that is needed to perform an SQL action on the
    object.

    For example, suppose that you are passing the reference for a table to a stored procedure that inserts rows into that table.
    Specify `'INSERT'` to confer the INSERT privilege on that table to the stored procedure.

    For a list of supported objects and privileges, see [Supported object types and privileges for references](/sql-reference/references#label-references-supported-objects-and-privileges).

    To specify more than one additional privilege, pass each privilege name as an additional argument to the function. For example,
    to confer the INSERT, UPDATE, and TRUNCATE privileges:

    Copy code

    ```
    CALL myprocedure( SYSTEM$REFERENCE('TABLE', 'table_with_different_owner', 'SESSION', 'INSERT'. 'UPDATE', 'TRUNCATE'));
    ```

    Note that you cannot specify OWNERSHIP or ALL as privileges.

## Returns

A serialized string representation of the reference that can be used as an identifier.

## Usage notes

The `'object_type'` argument must match the type of the object specified by `object_identifier`.

## Troubleshooting

The following scenarios can help you troubleshoot issues that can occur.

|  |  |
| --- | --- |
| Error | ``` 505028 (42601): Object type <object_type> does not match the specified type <type_of_the_specified_object> for reference creation ``` |
| Cause | If you try to create a reference using the SYSTEM$REFERENCE function and the `object_type` argument does not match the type of the object specified by `object_identifier`, the function fails. For example, if the `object_type` argument is TABLE, but `object_identifier` resolves to an object type other than TABLE (for example, VIEW), the function fails. |
| Solution | Verify that the type of the object specified by `object_identifier` matches the `object_type` argument. For a list of supported object types, see [Supported object types and privileges for references](/sql-reference/references#label-references-supported-objects-and-privileges). |

Expand

Show lessSee more

## Examples

See [Background: The problem with passing objects and queries to stored procedures](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-example).
