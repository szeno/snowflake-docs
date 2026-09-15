# May 22, 2024 — SQL Release Notes

## Using the TABLE keyword as an alternative to SYSTEM$REFERENCE and SYSTEM$QUERY\_REFERENCE

You can now use the TABLE keyword to get a
[reference](/developer-guide/stored-procedure/stored-procedures-calling-references) to a table, view, secure view, or query.

The reference created by this keyword is valid only for the scope of the call. In addition, the reference only confers the SELECT
privilege on the table, view, or secure view.

For example, rather than calling the [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function to get a reference to a table:

Copy code

```
CALL my_procedure(SYSTEM$REFERENCE('table', my_table));
```

you can use the TABLE keyword:

Copy code

```
CALL my_procedure(TABLE(my_table));
```

For details, see [Using the TABLE keyword to create a reference to a table, view, or query](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-table-keyword).
