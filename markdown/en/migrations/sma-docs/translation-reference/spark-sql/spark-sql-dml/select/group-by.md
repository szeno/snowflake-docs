description:
:   Will the SMA ever be in your GROUP BY clause?

# Snowpark Migration Accelerator: Group By

## Description

The `GROUP BY` clause groups rows based on specified expressions and calculates aggregate functions for each group. Databricks SQL provides advanced grouping options through `GROUPING SETS`, `CUBE`, and `ROLLUP` clauses, which allow multiple aggregations on the same dataset. You can combine regular grouping expressions with these advanced options in the `GROUP BY` clause, and nest them within `GROUPING SETS`. ([Databricks SQL Language Reference GROUP BY](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-groupby.html))

Groups rows that share the same values in specified columns and calculates aggregate functions (such as SUM, COUNT, or AVG) for each group. The GROUP BY clause can include:

- The name of a column
- A number that refers to a position in the [SELECT](https://docs.snowflake.com/en/sql-reference/sql/select) list
- Any valid expression

Extensions:

[GROUP BY CUBE](https://docs.snowflake.com/en/sql-reference/constructs/group-by-cube), [GROUP BY GROUPING SETS](https://docs.snowflake.com/en/sql-reference/constructs/group-by-grouping-sets), and [GROUP BY ROLLUP](https://docs.snowflake.com/en/sql-reference/constructs/group-by-rollup)

[Snowflake SQL Language Reference GROUP BY](https://docs.snowflake.com/en/sql-reference/constructs/group-by)

### Syntax

```
GROUP BY ALL

GROUP BY group_expression [, ...] [ WITH ROLLUP | WITH CUBE ]

GROUP BY { group_expression | { ROLLUP | CUBE | GROUPING SETS } ( grouping_set [, ...] ) } [, ...]

grouping_set
   { expression |
     ( [ expression [, ...] ] ) }
```

```
SELECT ...
  FROM ...
  [ ... ]
  GROUP BY groupItem [ , groupItem [ , ... ] ]
  [ ... ]

SELECT ...
  FROM ...
  [ ... ]
  GROUP BY ALL
  [ ... ]
groupItem ::= { <column_alias> | <position> | <expr> }

SELECT ...
FROM ...
[ ... ]
GROUP BY CUBE ( groupCube [ , groupCube [ , ... ] ] )
[ ... ]

groupCube ::= { <column_alias> | <position> | <expr> }

SELECT ...
FROM ...
[ ... ]
GROUP BY GROUPING SETS ( groupSet [ , groupSet [ , ... ] ] )
[ ... ]

groupSet ::= { <column_alias> | <position> | <expr> }

SELECT ...
FROM ...
[ ... ]
GROUP BY ROLLUP ( groupRollup [ , groupRollup [ , ... ] ] )
[ ... ]

groupRollup ::= { <column_alias> | <position> | <expr> }
```

## Sample Source Patterns

### Setup data

#### Databricks

Copy code

```
CREATE TEMP VIEW dealer (id, city, car_model, quantity) AS
VALUES (100, 'Fremont', 'Honda Civic', 10),
       (100, 'Fremont', 'Honda Accord', 15),
       (100, 'Fremont', 'Honda CRV', 7),
       (200, 'Dublin', 'Honda Civic', 20),
       (200, 'Dublin', 'Honda Accord', 10),
       (200, 'Dublin', 'Honda CRV', 3),
       (300, 'San Jose', 'Honda Civic', 5),
       (300, 'San Jose', 'Honda Accord', 8);
```

#### Snowflake

Copy code

```
CREATE TEMP TABLE dealer (id INT, city STRING, car_model STRING, quantity INT);
INSERT INTO dealer VALUES
        (100, 'Fremont', 'Honda Civic', 10),
        (100, 'Fremont', 'Honda Accord', 15),
        (100, 'Fremont', 'Honda CRV', 7),
        (200, 'Dublin', 'Honda Civic', 20),
        (200, 'Dublin', 'Honda Accord', 10),
        (200, 'Dublin', 'Honda CRV', 3),
        (300, 'San Jose', 'Honda Civic', 5),
        (300, 'San Jose', 'Honda Accord', 8);
```

### Pattern code

#### Databricks

Copy code

```
-- 1. Sum of quantity per dealership. Group by `id`.
SELECT id, sum(quantity) FROM dealer GROUP BY id ORDER BY id;

-- 2. Use column position in GROUP BY clause.
SELECT id, sum(quantity) FROM dealer GROUP BY 1 ORDER BY 1;

-- 3. Multiple aggregations.
-- 3.1. Sum of quantity per dealership.
-- 3.2. Max quantity per dealership.
SELECT id, sum(quantity) AS sum, max(quantity) AS max
    FROM dealer GROUP BY id ORDER BY id;

-- 4. Count the number of distinct dealers in cities per car_model.
SELECT car_model, count(DISTINCT city) AS count FROM dealer GROUP BY car_model;

-- 5. Count the number of distinct dealers in cities per car_model, using GROUP BY ALL
SELECT car_model, count(DISTINCT city) AS count FROM dealer GROUP BY ALL;

-- 6. Sum of only 'Honda Civic' and 'Honda CRV' quantities per dealership.
SELECT id,
         sum(quantity) FILTER (WHERE car_model IN ('Honda Civic', 'Honda CRV')) AS `sum(quantity)`
    FROM dealer
    GROUP BY id ORDER BY id;

-- 7. Aggregations using multiple sets of grouping columns in a single statement.
-- Following performs aggregations based on four sets of grouping columns.
-- 7.1. city, car_model
-- 7.2. city
-- 7.3. car_model
-- 7.4. Empty grouping set. Returns quantities for all city and car models.
SELECT city, car_model, sum(quantity) AS sum
    FROM dealer
    GROUP BY GROUPING SETS ((city, car_model), (city), (car_model), ())
    ORDER BY city;

-- 8. Group by processing with `ROLLUP` clause.
-- Equivalent GROUP BY GROUPING SETS ((city, car_model), (city), ())
SELECT city, car_model, sum(quantity) AS sum
    FROM dealer
    GROUP BY city, car_model WITH ROLLUP
    ORDER BY city, car_model;

-- 9. Group by processing with `CUBE` clause.
-- Equivalent GROUP BY GROUPING SETS ((city, car_model), (city), (car_model), ())
SELECT city, car_model, sum(quantity) AS sum
    FROM dealer
    GROUP BY city, car_model WITH CUBE
    ORDER BY city, car_model;
```

| id | sum(quantity) |
| --- | --- |
| 100 | 32 |
| 200 | 33 |
| 300 | 13 |

Expand

Show lessSee more

| id | sum(quantity) |
| --- | --- |
| 100 | 32 |
| 200 | 33 |
| 300 | 13 |

Expand

Show lessSee more

| id | sum | max |
| --- | --- | --- |
| 100 | 32 | 15 |
| 200 | 33 | 20 |
| 300 | 13 | 8 |

Expand

Show lessSee more

| car\_model | count |
| --- | --- |
| Honda Civic | 3 |
| Honda CRV | 2 |
| Honda Accord | 3 |

Expand

Show lessSee more

| car\_model | count |
| --- | --- |
| Honda Civic | 3 |
| Honda CRV | 2 |
| Honda Accord | 3 |

Expand

Show lessSee more

| id | sum(quantity) |
| --- | --- |
| 100 | 17 |
| 200 | 23 |
| 300 | 5 |

Expand

Show lessSee more

| city | car\_model | sum |
| --- | --- | --- |
| *NULL* | Honda Civic | 35 |
| *NULL* | Honda Accord | 33 |
| *NULL* | *NULL* | 78 |
| *NULL* | Honda CRV | 10 |
| Dublin | Honda Civic | 20 |
| Dublin | *NULL* | 33 |
| Dublin | Honda CRV | 3 |
| Dublin | Honda Accord | 10 |
| Fremont | Honda Accord | 15 |
| Fremont | Honda Civic | 10 |
| Fremont | *NULL* | 32 |
| Fremont | Honda CRV | 7 |
| San Jose | Honda Accord | 8 |
| San Jose | *NULL* | 13 |
| San Jose | Honda Civic | 5 |

Expand

Show lessSee more

| city | car\_model | sum |
| --- | --- | --- |
| *NULL* | *NULL* | 78 |
| Dublin | *NULL* | 33 |
| Dublin | Honda Accord | 10 |
| Dublin | Honda CRV | 3 |
| Dublin | Honda Civic | 20 |
| Fremont | *NULL* | 32 |
| Fremont | Honda Accord | 15 |
| Fremont | Honda CRV | 7 |
| Fremont | Honda Civic | 10 |
| San Jose | *NULL* | 13 |
| San Jose | Honda Accord | 8 |
| San Jose | Honda Civic | 5 |

Expand

Show lessSee more

| city | car\_model | sum |
| --- | --- | --- |
| *NULL* | *NULL* | 78 |
| *NULL* | Honda Accord | 33 |
| *NULL* | Honda CRV | 10 |
| *NULL* | Honda Civic | 35 |
| Dublin | *NULL* | 33 |
| Dublin | Honda Accord | 10 |
| Dublin | Honda CRV | 3 |
| Dublin | Honda Civic | 20 |
| Fremont | *NULL* | 32 |
| Fremont | Honda Accord | 15 |
| Fremont | Honda CRV | 7 |
| Fremont | Honda Civic | 10 |
| San Jose | *NULL* | 13 |
| San Jose | Honda Accord | 8 |
| San Jose | Honda Civic | 5 |

Expand

Show lessSee more

#### Snowflake

Copy code

```
-- 1. Sum of quantity per dealership. Group by `id`.
SELECT id, sum(quantity) FROM dealer GROUP BY id ORDER BY id;

-- 2. Use column position in GROUP BY clause.
SELECT id, sum(quantity) FROM dealer GROUP BY 1 ORDER BY 1;

-- 3. Multiple aggregations.
-- 3.1. Sum of quantity per dealership.
-- 3.2. Max quantity per dealership.
SELECT id, sum(quantity) AS sum, max(quantity) AS max
    FROM dealer GROUP BY id ORDER BY id;

-- 4. Count the number of distinct dealers in cities per car_model.
SELECT car_model, count(DISTINCT city) AS count FROM dealer GROUP BY car_model;

-- 5. Count the number of distinct dealers in cities per car_model, using GROUP BY ALL
SELECT car_model, count(DISTINCT city) AS count FROM dealer GROUP BY ALL;

-- 6. Sum of only 'Honda Civic' and 'Honda CRV' quantities per dealership.
SELECT
    id,
    SUM(CASE WHEN car_model='Honda Civic' OR car_model='Honda CRV' THEN quantity ELSE NULL END) AS `sum(quantity)`
    FROM dealer
    GROUP BY id ORDER BY id;

-- 7. Aggregations using multiple sets of grouping columns in a single statement.
-- Following performs aggregations based on four sets of grouping columns.
-- 7.1. city, car_model
-- 7.2. city
-- 7.3. car_model
-- 7.4. Empty grouping set. Returns quantities for all city and car models.
SELECT city, car_model, sum(quantity) AS sum
    FROM dealer
    GROUP BY GROUPING SETS ((city, car_model), (city), (car_model), ())
    ORDER BY city NULLS FIRST;

-- 8. Group by processing with `ROLLUP` clause.
-- Equivalent GROUP BY GROUPING SETS ((city, car_model), (city), ())
SELECT city, car_model, sum(quantity) AS sum
    FROM dealer
    GROUP BY ROLLUP (city, car_model)
    ORDER BY city NULLS FIRST, car_model NULLS FIRST;

-- 9. Group by processing with `CUBE` clause.
-- Equivalent GROUP BY GROUPING SETS ((city, car_model), (city), (car_model), ())
SELECT city, car_model, sum(quantity) AS sum
    FROM dealer
    GROUP BY CUBE (city, car_model)
    ORDER BY city NULLS FIRST, car_model NULLS FIRST;
```

| id | sum(quantity) |
| --- | --- |
| 100 | 32 |
| 200 | 33 |
| 300 | 13 |

Expand

Show lessSee more

| id | sum(quantity) |
| --- | --- |
| 100 | 32 |
| 200 | 33 |
| 300 | 13 |

Expand

Show lessSee more

| id | sum | max |
| --- | --- | --- |
| 100 | 32 | 15 |
| 200 | 33 | 20 |
| 300 | 13 | 8 |

Expand

Show lessSee more

| car\_model | count |
| --- | --- |
| Honda Civic | 3 |
| Honda CRV | 2 |
| Honda Accord | 3 |

Expand

Show lessSee more

| car\_model | count |
| --- | --- |
| Honda Civic | 3 |
| Honda CRV | 2 |
| Honda Accord | 3 |

Expand

Show lessSee more

| id | sum(quantity) |
| --- | --- |
| 100 | 17 |
| 200 | 23 |
| 300 | 5 |

Expand

Show lessSee more

| city | car\_model | sum |
| --- | --- | --- |
| *NULL* | Honda Civic | 35 |
| *NULL* | Honda Accord | 33 |
| *NULL* | *NULL* | 78 |
| *NULL* | Honda CRV | 10 |
| Dublin | Honda Civic | 20 |
| Dublin | *NULL* | 33 |
| Dublin | Honda CRV | 3 |
| Dublin | Honda Accord | 10 |
| Fremont | Honda Accord | 15 |
| Fremont | Honda Civic | 10 |
| Fremont | *NULL* | 32 |
| Fremont | Honda CRV | 7 |
| San Jose | Honda Accord | 8 |
| San Jose | *NULL* | 13 |
| San Jose | Honda Civic | 5 |

Expand

Show lessSee more

| city | car\_model | sum |
| --- | --- | --- |
| *NULL* | *NULL* | 78 |
| Dublin | *NULL* | 33 |
| Dublin | Honda Accord | 10 |
| Dublin | Honda CRV | 3 |
| Dublin | Honda Civic | 20 |
| Fremont | *NULL* | 32 |
| Fremont | Honda Accord | 15 |
| Fremont | Honda CRV | 7 |
| Fremont | Honda Civic | 10 |
| San Jose | *NULL* | 13 |
| San Jose | Honda Accord | 8 |
| San Jose | Honda Civic | 5 |

Expand

Show lessSee more

| city | car\_model | sum |
| --- | --- | --- |
| *NULL* | *NULL* | 78 |
| *NULL* | Honda Accord | 33 |
| *NULL* | Honda CRV | 10 |
| *NULL* | Honda Civic | 35 |
| Dublin | *NULL* | 33 |
| Dublin | Honda Accord | 10 |
| Dublin | Honda CRV | 3 |
| Dublin | Honda Civic | 20 |
| Fremont | *NULL* | 32 |
| Fremont | Honda Accord | 15 |
| Fremont | Honda CRV | 7 |
| Fremont | Honda Civic | 10 |
| San Jose | *NULL* | 13 |
| San Jose | Honda Accord | 8 |
| San Jose | Honda Civic | 5 |

Expand

Show lessSee more

### Known Issues

No issues were found

### Related EWIs

No related EWIs
