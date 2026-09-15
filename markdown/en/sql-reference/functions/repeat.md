Categories:
:   [String & binary functions](/sql-reference/functions-string) (General)

# REPEAT

Builds a string by repeating the input for the specified number of
times.

## Syntax

Copy code

```
REPEAT(<input>, <n>)
```

## Arguments

`input`
:   The input string from which the output string is built.

`n`
:   The number of times the input string should be repeated. The minimum
    valid number is 0 (which results in an empty string).

## Examples

Copy code

```
SELECT REPEAT('xy', 5);

-----------------+
 REPEAT('XY', 5) |
-----------------+
 xyxyxyxyxy      |
-----------------+
```
