Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$REMOVE\_REFERENCE

Remove an association from the reference to an object in the consumer account and returns
a unique system-generated alias for the reference.

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

`'reference_string'`
:   The system-generated ID of the reference to the object in the consumer account.
