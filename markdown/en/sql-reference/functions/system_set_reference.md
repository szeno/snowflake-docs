Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$SET\_REFERENCE

Called by a Snowflake Native App to associate a consumer reference string to a reference definition.
The app can use this association to access the consumer object. The reference string passed to this system function is the value returned by the
[SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function, which represents a consumer object.

This function only supports a single-valued reference. If an association has already been created using the same reference name, the existing association is overwritten.

## Syntax

Copy code

```
SYSTEM$SET_REFERENCE('<reference_name>', '<reference_string>')
```

## Arguments

**Required**

`'reference_name'`
:   The name of the reference as specified in the `manifest.yml` file of the app.

`'reference_string'`
:   The system-generated ID of the reference to the object in the consumer account.

## Returns

Returns a `VARCHAR` value that contains the system-generated alias for the association.

## Examples

This example assumes that the app manifest defines a single-valued `consumer_table` reference
with object type `TABLE` and the `SELECT` privilege. The app’s setup script must also create
the `config` schema and `app_admin` application role and grant `USAGE` on the schema to that role.
For the manifest and setup-script prerequisites, see [Request references and object-level privileges from consumers](/developer-guide/native-apps/requesting-refs).

Add this procedure to the app’s setup script:

Copy code

```
CREATE PROCEDURE config.set_table_reference(ref_name VARCHAR, ref_string VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SQL
  EXECUTE AS OWNER
  AS
  $$
  DECLARE
    association_alias VARCHAR;
  BEGIN
    association_alias := (SELECT SYSTEM$SET_REFERENCE(:ref_name, :ref_string));
    RETURN association_alias;
  END;
  $$;

GRANT USAGE ON PROCEDURE config.set_table_reference(VARCHAR, VARCHAR)
  TO APPLICATION ROLE app_admin;
```

After installing the app as `my_app`, a consumer whose role can create the reference and has
the `my_app.app_admin` application role can associate an existing table with `consumer_table`:

Copy code

```
SET table_reference = (
  SELECT SYSTEM$REFERENCE('TABLE', 'consumer_db.public.orders', 'PERSISTENT', 'SELECT')
);

CALL my_app.config.set_table_reference('consumer_table', $table_reference);
```

The procedure returns a UUID alias, for example:

```
6f3b7c2a-9d41-4e8f-a625-1b0c7d9e2345
```

To replace the association with a different existing table, create a reference to that table
and call the procedure again:

Copy code

```
SET replacement_reference = (
  SELECT SYSTEM$REFERENCE('TABLE', 'consumer_db.public.orders_archive', 'PERSISTENT', 'SELECT')
);

CALL my_app.config.set_table_reference('consumer_table', $replacement_reference);
```

The second call replaces the existing association and returns a new system-generated alias.
The UUID shown here is illustrative, not a fixed return value.
