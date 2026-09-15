Categories:
:   [System functions](/sql-reference/functions-system) (Information)

# SYSTEM$QUERY\_REFERENCE

Returns a [query reference](/developer-guide/stored-procedure/stored-procedures-calling-references) that you can pass to a stored procedure.
Within the stored procedure, when you execute the query, the query is performed using the role of the user who created the query
reference.

Note

As an alternative to calling this function, you can use the TABLE keyword, if you want the reference to be valid for the scope
of the call (rather than for the entire session). See [Using the TABLE keyword to create a reference to a table, view, or query](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-table-keyword).

See also:
:   [SYSTEM$REFERENCE](/sql-reference/functions/system_reference)

## Syntax

Copy code

```
SYSTEM$QUERY_REFERENCE('<select_statement>', [ , <use_session_scope> ] )
```

## Arguments

**Required**

`select_statement`
:   The SELECT statement to pass to the stored procedure. This must be a statement that serves as an inline view.

    Note that if the SELECT statement contains any single quotes or other special characters (e.g. newlines), you must
    [escape those characters with backslashes](/sql-reference/data-types-text#label-single-quoted-string-constants-escape-sequences).

**Optional**

`use_session_scope`
:   If `TRUE`, specifies that the query reference should be valid for the duration for the session. If this is `FALSE`
    or omitted, the query reference is valid within the context in which it was created. See [Specifying the scope of the reference](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-scope).

    Default value: `FALSE`

## Returns

A query reference that represents the specified SELECT statement.

## Usage notes

## Examples

See [Using query references](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-query-references).
