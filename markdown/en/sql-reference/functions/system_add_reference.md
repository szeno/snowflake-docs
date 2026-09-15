Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ADD\_REFERENCE

Called by a Snowflake Native App to associate a consumer reference string to a reference definition. The app can use this
association to access the consumer object. The reference string passed to this system function is the value returned by the
[SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function, which represents a consumer object.

For information about using this function in an app, see
[Request references and object-level privileges from consumers](/developer-guide/native-apps/requesting-refs).

This function supports both single and multi-valued references. The function returns an
error if an association has already been created using the same value specified by
`reference_name`.

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
