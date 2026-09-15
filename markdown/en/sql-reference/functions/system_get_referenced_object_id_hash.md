Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_REFERENCED\_OBJECT\_ID\_HASH

Returns the hash of the entity ID of the consumer object. This is the identifier of the entity resolved originally when a reference was created.

This function is useful for an app to determine whether the object bound to a reference has changed. The app can save the value and then compare the current value to the previously known value.

## Syntax

Copy code

```
SYSTEM$GET_REFERENCED_OBJECT_ID_HASH('<reference_name>'[, '<alias>'])
```

## Arguments

**Required**

`'reference_name'`
:   The name of the reference as specified in the `manifest.yml` file of the app.

`'reference_string'`
:   The system-generated ID of the reference to the object in the consumer account.
