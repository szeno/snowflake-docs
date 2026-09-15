Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$TYPEOF

Returns a string representing the SQL data type associated with an
expression.

See also:
:   [TYPEOF](/sql-reference/functions/typeof)

## Syntax

Copy code

```
SYSTEM$TYPEOF( <expr> )
```

## Arguments

`expr`
:   The argument can be a column name or a general expression.

## Returns

Returns a VARCHAR value that contains the data type of the input expression, for example, BOOLEAN, NUMBER, ARRAY, OBJECT, etc.

## Usage notes

- If TYPEOF is executed without the SYSTEM$ prefix (i.e. as a regular
  function rather than a system function), it returns different
  results (see [TYPEOF](/sql-reference/functions/typeof)).

## Examples

Copy code

```
SELECT SYSTEM$TYPEOF(NULL);
```

```
+---------------------+
| SYSTEM$TYPEOF(NULL) |
|---------------------|
| NULL[LOB]           |
+---------------------+
```

Copy code

```
SELECT SYSTEM$TYPEOF(1);
```

```
+------------------+
| SYSTEM$TYPEOF(1) |
|------------------|
| NUMBER(1,0)[SB1] |
+------------------+
```

Copy code

```
SELECT SYSTEM$TYPEOF(1e10);
```

```
+---------------------+
| SYSTEM$TYPEOF(1E10) |
|---------------------|
| NUMBER(11,0)[SB8]   |
+---------------------+
```

Copy code

```
SELECT SYSTEM$TYPEOF(10000);
```

```
+----------------------+
| SYSTEM$TYPEOF(10000) |
|----------------------|
| NUMBER(5,0)[SB2]     |
+----------------------+
```

Copy code

```
SELECT SYSTEM$TYPEOF('something');
```

```
+----------------------------+
| SYSTEM$TYPEOF('SOMETHING') |
|----------------------------|
| VARCHAR(9)[LOB]            |
+----------------------------+
```

Copy code

```
SELECT SYSTEM$TYPEOF(CONCAT('every', 'body'));
```

```
+----------------------------------------+
| SYSTEM$TYPEOF(CONCAT('EVERY', 'BODY')) |
|----------------------------------------|
| VARCHAR(9)[LOB]                        |
+----------------------------------------+
```
