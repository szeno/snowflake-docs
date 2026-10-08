Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$REMOVE\_ALL\_REFERENCES

Deletes all associations to the reference.

## Syntax

Copy code

```
SYSTEM$REMOVE_ALL_REFERENCES('<reference_name>')
```

## Arguments

**Required**

`'reference_name'`
:   The name of the reference as specified in the `manifest.yml` file of the app.

## Returns

Returns a `VARCHAR` value that contains a message confirming that all associations to the reference were removed.

## Examples

This example assumes that the app manifest defines `consumer_tables`. The reference can be
single-valued or multi-valued. Add this procedure to the app’s setup script. The `config`
schema and `app_admin` application role must already exist, with `USAGE` on the schema
granted to the role. See [Request references and object-level privileges from consumers](/developer-guide/native-apps/requesting-refs) for the prerequisites:

Copy code

```
CREATE PROCEDURE config.clear_table_references(ref_name VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SQL
  EXECUTE AS OWNER
  AS
  $$
  DECLARE
    status_message VARCHAR;
  BEGIN
    status_message := (SELECT SYSTEM$REMOVE_ALL_REFERENCES(:ref_name));
    RETURN status_message;
  END;
  $$;

GRANT USAGE ON PROCEDURE config.clear_table_references(VARCHAR)
  TO APPLICATION ROLE app_admin;
```

After installing the app as `my_app`, a consumer with the `my_app.app_admin` application role
clears the associations:

Copy code

```
CALL my_app.config.clear_table_references('consumer_tables');
```

The procedure returns a status message. It removes the associations, not the consumer objects
or the reference definition in the manifest. A subsequent call to
[SYSTEM$GET\_ALL\_REFERENCES](/sql-reference/functions/system_get_all_references) for `consumer_tables` returns `[]`.
