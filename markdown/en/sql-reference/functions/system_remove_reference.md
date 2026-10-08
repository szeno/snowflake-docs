Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$REMOVE\_REFERENCE

Removes an association from the reference to an object in the consumer account.

This function supports both single and multi-valued references. For multi-valued references,
an alias to the reference is required. This alias is used to remove a single association. To
remove all associations of a multi-valued reference, use [SYSTEM$REMOVE\_ALL\_REFERENCES](/sql-reference/functions/system_remove_all_references).

## Syntax

Copy code

```
SYSTEM$REMOVE_REFERENCE('<reference_name>'[, '<alias>'])
```

## Arguments

**Required**

`'reference_name'`
:   The name of the reference as specified in the `manifest.yml` file of the app.

**Optional**

`'alias'`
:   The system-generated alias of the association. This argument is required for a multi-valued reference.
    To get the aliases of the associations for a reference, call
    [SYSTEM$GET\_ALL\_REFERENCES](/sql-reference/functions/system_get_all_references).

## Returns

Returns a `VARCHAR` value that contains a message confirming that the association was removed.

## Examples

### Remove one association from a multi-valued reference

This example assumes that the app has a multi-valued `consumer_tables` reference with at least
one association. Use the alias returned by [SYSTEM$ADD\_REFERENCE](/sql-reference/functions/system_add_reference)
or [SYSTEM$GET\_ALL\_REFERENCES](/sql-reference/functions/system_get_all_references), not the reference string returned
by [SYSTEM$REFERENCE](/sql-reference/functions/system_reference).

Add this procedure to the app’s setup script. The `config` schema and `app_admin` application
role must already exist, with `USAGE` on the schema granted to the role. See
[Request references and object-level privileges from consumers](/developer-guide/native-apps/requesting-refs) for the setup-script prerequisites:

Copy code

```
CREATE PROCEDURE config.remove_table_reference(ref_name VARCHAR, association_alias VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SQL
  EXECUTE AS OWNER
  AS
  $$
  DECLARE
    status_message VARCHAR;
  BEGIN
    status_message := (SELECT SYSTEM$REMOVE_REFERENCE(:ref_name, :association_alias));
    RETURN status_message;
  END;
  $$;

GRANT USAGE ON PROCEDURE config.remove_table_reference(VARCHAR, VARCHAR)
  TO APPLICATION ROLE app_admin;
```

After installing the app as `my_app`, a consumer with the `my_app.app_admin` application role
calls the procedure with an existing alias. Replace the illustrative UUID with the alias
for the association to remove:

Copy code

```
CALL my_app.config.remove_table_reference(
  'consumer_tables', '6f3b7c2a-9d41-4e8f-a625-1b0c7d9e2345'
);
```

The procedure returns a status message. Other associations for `consumer_tables` remain.
The consumer table itself isn’t dropped.

### Remove a single-valued association without an alias

For a single-valued reference, an app-owned procedure can omit the alias. For example,
use the following statement in the procedure body to remove the association for
`consumer_table`:

Copy code

```
SELECT SYSTEM$REMOVE_REFERENCE('consumer_table');
```

If no association exists, the function returns an error rather than a success message.
