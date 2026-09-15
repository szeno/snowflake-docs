Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# CONCAT\_WS

Concatenates two or more strings, or concatenates two or more binary values, and uses
the first argument as a delimiter between the following strings.

Note

Unlike some implementations of the CONCAT\_WS function, the Snowflake CONCAT\_WS function
doesn’t skip NULL values.

See also:
:   [CONCAT](/sql-reference/functions/concat)

## Syntax

Copy code

```
CONCAT_WS( <separator> , <expression> [ , <expression> ... ] )
```

## Arguments

`separator`
:   The separator must meet the same requirements as `expression`.

`expression`
:   The input expressions must be all strings, or all binary values.

## Returns

The function returns a VARCHAR or BINARY value that contains the 2nd through Nth arguments,
separated by the first argument.

If any argument is NULL, the function returns NULL.

The data type of the returned value is the same as the data type of the input values.

## Usage notes

- Metadata functions such as [GET\_DDL](/sql-reference/functions/get_ddl) accept only constants as input. Concatenated
  input generates an error.
- CONCAT\_WS puts separators between arguments, not after the last argument. If CONCAT\_WS is called
  with only one argument after the separator, then no separator is appended.

## Collation details

- The [collation specifications](/sql-reference/collation#label-collation-specification) of all input arguments must be compatible.
- The collation of the result of the function is the highest-[precedence](/sql-reference/collation#label-determining-the-collation-used-in-an-operation) collation of the inputs.

## Examples

Call the CONCAT\_WS function to concatenate three strings with a comma separator:

Copy code

```
SELECT CONCAT_WS(',', 'one', 'two', 'three');
```

```
+---------------------------------------+
| CONCAT_WS(',', 'ONE', 'TWO', 'THREE') |
|---------------------------------------|
| one,two,three                         |
+---------------------------------------+
```

The following example shows that if any argument is NULL, the function returns NULL:

Copy code

```
SELECT CONCAT_WS(',', 'one', NULL, 'two');
```

```
+------------------------------------+
| CONCAT_WS(',', 'ONE', NULL, 'TWO') |
|------------------------------------|
| NULL                               |
+------------------------------------+
```

The following example shows that when there is only one string to concatenate, the CONCAT\_WS function
doesn’t append a separator:

Copy code

```
SELECT CONCAT_WS(',', 'one');
```

```
+-----------------------+
| CONCAT_WS(',', 'ONE') |
|-----------------------|
| one                   |
+-----------------------+
```
