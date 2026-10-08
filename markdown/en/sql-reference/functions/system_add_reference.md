Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ADD\_REFERENCE

Called by a Snowflake Native App to associate a consumer reference string to a reference definition. The app can use this
association to access the consumer object. The reference string passed to this system function is the value returned by the
[SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function, which represents a consumer object.

For information about using this function in an app, see
[Request references and object-level privileges from consumers](/developer-guide/native-apps/requesting-refs).

This function supports both single-valued and multi-valued references. For a single-valued
reference, the function returns an error if an association already exists. To replace that
association, use [SYSTEM$SET\_REFERENCE](/sql-reference/functions/system_set_reference).

## Syntax

Copy code

```
SYSTEM$ADD_REFERENCE('<reference_name>', '<reference_string>')
```

## Arguments

`'reference_name'`
:   The name of the reference as specified in the `manifest.yml` file of the app.

`'reference_string'`
:   The system-generated ID of the reference to the object in the consumer account.

## Returns

Returns a `VARCHAR` value that contains the system-generated alias for the new association.
For a multi-valued reference, pass this alias to [SYSTEM$REMOVE\_REFERENCE](/sql-reference/functions/system_remove_reference)
or [SYSTEM$GET\_REFERENCED\_OBJECT\_ID\_HASH](/sql-reference/functions/system_get_referenced_object_id_hash) to identify a single association.

## Examples

This example assumes that the app manifest defines a multi-valued `consumer_tables` reference
with object type `TABLE` and the `SELECT` privilege. The app’s setup script must also create
the `config` schema and `app_admin` application role and grant `USAGE` on the schema to that role.
For the manifest and setup-script prerequisites, see [Request references and object-level privileges from consumers](/developer-guide/native-apps/requesting-refs).

Add this procedure to the app’s setup script. It runs with the app’s privileges and returns
the alias of the new association:

Copy code

```
CREATE PROCEDURE config.add_table_reference(ref_name VARCHAR, ref_string VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SQL
  EXECUTE AS OWNER
  AS
  $$
  DECLARE
    association_alias VARCHAR;
  BEGIN
    association_alias := (SELECT SYSTEM$ADD_REFERENCE(:ref_name, :ref_string));
    RETURN association_alias;
  END;
  $$;

GRANT USAGE ON PROCEDURE config.add_table_reference(VARCHAR, VARCHAR)
  TO APPLICATION ROLE app_admin;
```

After installing the app as `my_app`, the consumer creates a persistent reference to an
existing table and passes it to the procedure. The consumer’s role must have the privileges
needed to create the reference and must be granted the `my_app.app_admin` application role:

Copy code

```
SET table_reference = (
  SELECT SYSTEM$REFERENCE('TABLE', 'consumer_db.public.orders', 'PERSISTENT', 'SELECT')
);

CALL my_app.config.add_table_reference('consumer_tables', $table_reference);
```

The procedure returns a UUID alias, for example:

```
6f3b7c2a-9d41-4e8f-a625-1b0c7d9e2345
```

The alias is illustrative. Each association has its own system-generated alias. Repeat the
consumer statements with a different table to add another association to `consumer_tables`.
