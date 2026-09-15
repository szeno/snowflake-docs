Categories:
:   [Query syntax](/sql-reference/constructs)

# INTO

Sets [Snowflake Scripting variables](/developer-guide/snowflake-scripting/variables) to the values in a row returned by a
SELECT statement. See [Setting variables to the results of a SELECT statement](/developer-guide/snowflake-scripting/variables#label-snowscript-variables-select-into) for details.

## Syntax

Copy code

```
SELECT <expression1>
   [ , <expression2> ]
   [ , <expressionN> ]
[ INTO :<variable1> ]
   [ , :<variable2> ]
   [ , :<variableN> ]
FROM ...
WHERE ...
[ ... ]
```

## Parameters

`expression1`, `expression2`, `expressionN`
:   Specifies scalar expressions (e.g. columns in a table specified by the [FROM](/sql-reference/constructs/from) clause).

`variable1`, `variable2`, `variableN`
:   [Snowflake Scripting variables](/developer-guide/snowflake-scripting/variables) that should be set to the values in the
    expressions in the SELECT clause.

## Usage notes

- The SELECT statement must return a single row.

## Examples

See [Setting variables to the results of a SELECT statement](/developer-guide/snowflake-scripting/variables#label-snowscript-variables-select-into).
