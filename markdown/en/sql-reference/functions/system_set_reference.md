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
