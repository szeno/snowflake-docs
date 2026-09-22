description:
:   Let’s share core values sometime

# Snowpark Migration Accelerator: Values

## Description

Creates a temporary table within the query that can be used immediately. For more information, see [Databricks SQL Language Reference VALUES](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-values.html).

The VALUES sub-clause in a SELECT statement’s FROM clause lets you define a set of fixed values to create a specific number of rows. ([Snowflake SQL Language Reference VALUES](https://docs.snowflake.com/en/sql-reference/constructs/values))

### Syntax

Copy code

```
VALUES {expression | ( expression [, ...] ) } [, ...] [table_alias]

SELECT expression [, ...] [table_alias]
```

Copy code

```
SELECT ...
FROM ( VALUES ( <expr> [ , <expr> [ , ... ] ] ) [ , ( ... ) ] ) [ [ AS ] <table_alias> [ ( <column_alias> [, ... ] ) ] ]
[ ... ]
```

## Sample Source Patterns

### Setup data

#### Databricks

Copy code

```
CREATE TEMPORARY VIEW number1(c) AS VALUES (3), (1), (2), (2), (3), (4);
```

#### Snowflake

Copy code

```
CREATE TEMPORARY TABLE number1(c int);
INSERT INTO number1 VALUES (3), (1), (2), (2), (3), (4);
```

### Pattern code

#### Databricks

Copy code

```
-- single row, without a table alias
> VALUES ("one", 1);
  one    1

-- Multiple rows, one column
> VALUES 1, 2, 3;
 1
 2
 3

-- three rows with a table alias
> SELECT data.a, b
    FROM VALUES ('one', 1),
                ('two', 2),
                ('three', NULL) AS data(a, b);
   one    1
   two    2
 three NULL

-- complex types with a table alias
> SELECT a, b
  FROM VALUES ('one', array(0, 1)),
              ('two', array(2, 3)) AS data(a, b);
 one [0, 1]
 two [2, 3]

-- Using the SELECT syntax
> SELECT 'one', 2
 one 2
```

| c |
| --- |
| 3 |
| 1 |
| 2 |
| 4 |

Expand

Show lessSee more

#### Snowflake

Copy code

```
-- single row, without a table alias
SELECT * FROM (VALUES ('one', 1));

-- Multiple rows, one column
SELECT * FROM (VALUES (1), (2), (3));

-- three rows with a table alias
SELECT a, b
    FROM (VALUES ('one', 1),
                ('two', 2),
                ('three', NULL)) AS data(a, b);

-- complex types with a table alias
SELECT a, b
    FROM
    (VALUES ('one', '[0, 1]'),
            ('two', '[2, 3]')
            ) AS data(a, b);

-- Using the SELECT syntax
SELECT 'one', 2
```

| c |
| --- |
| 3 |
| 1 |
| 2 |
| 4 |

Expand

Show lessSee more

### Known Issues

No issues were found

### Related EWIs

No related EWIs
