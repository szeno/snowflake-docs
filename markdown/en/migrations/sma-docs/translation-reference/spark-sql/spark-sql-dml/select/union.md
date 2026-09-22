description:
:   Snowflake and Snowpark. Has there ever been a more perfect union?

# Snowpark Migration Accelerator: Union

## Description

Merges two subqueries into a single query. Databricks SQL provides three set operators that allow you to combine queries:

- `EXCEPT` - Retrieves all rows from the first query that do not appear in the second query
- `INTERSECT` - Returns only the rows that appear in both queries
- `UNION` - Combines the results of two or more queries into a single result set

[Databricks SQL Language Reference UNION](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-setops.html)

Set operators enable you to combine multiple queries into a single result. For more details, see [Snowflake SQL Language Reference UNION](https://docs.snowflake.com/en/sql-reference/operators-query).

### Syntax

Copy code

```
subquery1 { { UNION [ ALL | DISTINCT ] |
              INTERSECT [ ALL | DISTINCT ] |
              EXCEPT [ ALL | DISTINCT ] } subquery2 } [...] }
```

Copy code

```
[ ( ] <query> [ ) ] { INTERSECT | { MINUS | EXCEPT } | UNION [ ALL ] } [ ( ] <query> [ ) ]
[ ORDER BY ... ]
[ LIMIT ... ]
```

## Sample Source Patterns

### Setup data

#### Databricks

Copy code

```
CREATE TEMPORARY VIEW number1(c) AS VALUES (3), (1), (2), (2), (3), (4);

CREATE TEMPORARY VIEW number2(c) AS VALUES (5), (1), (1), (2);
```

#### Snowflake

Copy code

```
CREATE TEMPORARY TABLE number1(c int);
INSERT INTO number1 VALUES (3), (1), (2), (2), (3), (4);

CREATE TEMPORARY TABLE number2(c int);
INSERT INTO number2 VALUES (5), (1), (1), (2);
```

### Pattern code

#### Databricks

Copy code

```
-- EXCEPT (MINUS) Operator:
SELECT c FROM number1 EXCEPT SELECT c FROM number2;

SELECT c FROM number1 MINUS SELECT c FROM number2;

-- EXCEPT ALL (MINUS ALL) Operator:
SELECT c FROM number1 EXCEPT ALL (SELECT c FROM number2);

SELECT c FROM number1 MINUS ALL (SELECT c FROM number2);

-- INTERSECT Operator:
(SELECT c FROM number1) INTERSECT (SELECT c FROM number2);

-- INTERSECT DISTINCT Operator:
(SELECT c FROM number1) INTERSECT DISTINCT (SELECT c FROM number2);

-- INTERSECT ALL Operator:
(SELECT c FROM number1) INTERSECT ALL (SELECT c FROM number2);

-- UNION Operator:
(SELECT c FROM number1) UNION (SELECT c FROM number2);

-- UNION DISTINCT Operator:
(SELECT c FROM number1) UNION DISTINCT (SELECT c FROM number2);

-- UNION ALL Operator:
SELECT c FROM number1 UNION ALL (SELECT c FROM number2);
```

**EXCEPT (MINUS) Operator:** The EXCEPT operator, also known as MINUS, removes rows from the first query that appear in the result set of the second query. It returns only unique rows from the first query that do not exist in the second query.

| c |
| --- |
| 3 |
| 4 |

Expand

Show lessSee more

**EXCEPT ALL (MINUS ALL) Operator: Removes Duplicate Records**

| c |
| --- |
| 3 |
| 3 |
| 4 |

Expand

Show lessSee more

**INTERSECT Operator:** Returns only the rows that appear in both result sets, eliminating duplicates. It compares the results of two or more SELECT statements and returns only the matching records.

| c |
| --- |
| 1 |
| 2 |

Expand

Show lessSee more

**INTERSECT DISTINCT Operator:** Returns only unique rows that appear in both result sets, eliminating any duplicates.

| c |
| --- |
| 1 |
| 2 |

Expand

Show lessSee more

**INTERSECT ALL Operator:** Returns all matching rows from multiple queries, including duplicates. Unlike the standard INTERSECT operator, which removes duplicates, INTERSECT ALL preserves duplicate rows in the final result set.

| c |
| --- |
| 1 |
| 2 |
| 2 |

Expand

Show lessSee more

**UNION Operator:** The UNION operator combines the results of two or more SELECT statements into a single result set. It removes duplicate rows from the combined result set by default.

| c |
| --- |
| 1 |
| 3 |
| 5 |
| 4 |
| 2 |

Expand

Show lessSee more

**UNION DISTINCT Operator:** The UNION DISTINCT operator combines two or more result sets and removes any duplicate rows from the final output. It returns only unique rows from all the combined queries.

| c |
| --- |
| 1 |
| 3 |
| 5 |
| 4 |
| 2 |

Expand

Show lessSee more

**UNION ALL Operator:** The UNION ALL operator combines rows from two or more queries without removing duplicate records. Unlike the UNION operator, UNION ALL retains all rows, including duplicates, making it faster to execute since it doesn’t need to perform duplicate checking.

| c |
| --- |
| 3 |
| 1 |
| 2 |
| 2 |
| 3 |
| 4 |
| 5 |
| 1 |
| 1 |
| 2 |

Expand

Show lessSee more

#### Snowflake

Copy code

```
-- EXCEPT (MINUS) Operator
SELECT c FROM number1 EXCEPT SELECT c FROM number2;

SELECT c FROM number1 MINUS SELECT c FROM number2;

-- EXCEPT ALL (MINUS ALL) Operator:
SELECT number1.c FROM number1
LEFT JOIN number2
    ON number1.c = number2.c
WHERE number2.c IS NULL;
-- ** MSC-WARMING - MSC-S000# - EXCEPT ALL IS TRANSFORMED TO A LEFT JOIN. **

SELECT number1.c FROM number1
LEFT JOIN number2
    ON number1.c = number2.c
WHERE number2.c IS NULL;
-- ** MSC-WARMING - MSC-S000# - MINUS ALL IS TRANSFORMED TO A LEFT JOIN. **

-- INTERSECT Operator:
(SELECT c FROM number1) INTERSECT (SELECT c FROM number2);

-- INTERSECT DISTINCT Operator:
(SELECT c FROM number1) INTERSECT (SELECT c FROM number2);

-- INTERSECT ALL Operator:
SELECT DISTINCT number1.c FROM number1
INNER JOIN number2
    ON number1.c = number2.c;
-- ** MSC-WARMING - MSC-S000# - INTERSECT ALL IS TRANSFORMED TO A INNER JOIN. **

-- UNION Operator:
(SELECT c FROM number1) UNION (SELECT c FROM number2);

-- UNION DISTINCT Operator:
(SELECT c FROM number1) UNION DISTINCT (SELECT c FROM number2);

-- UNION ALL Operator:
SELECT c FROM number1 UNION ALL (SELECT c FROM number2);
```

**EXCEPT (MINUS) Operator: Removes Duplicate Records**

The EXCEPT operator, also known as MINUS, compares two queries and returns only the unique records from the first query that do not appear in the second query. It eliminates duplicate rows from the result set.

| c |
| --- |
| 3 |
| 4 |

Expand

Show lessSee more

**EXCEPT ALL (MINUS ALL) Operator: Removes Duplicate Rows**

| c |
| --- |
| 3 |
| 3 |
| 4 |

Expand

Show lessSee more

**INTERSECT Operator:**

| c |
| --- |
| 1 |
| 2 |

Expand

Show lessSee more

**INTERSECT DISTINCT Operator:**

| c |
| --- |
| 1 |
| 2 |

Expand

Show lessSee more

**INTERSECT ALL Operator:**

| c |
| --- |
| 1 |
| 2 |
| 2 |

Expand

Show lessSee more

**UNION Operator:**

| c |
| --- |
| 1 |
| 3 |
| 5 |
| 4 |
| 2 |

Expand

Show lessSee more

**UNION DISTINCT Operator:**

| c |
| --- |
| 1 |
| 3 |
| 5 |
| 4 |
| 2 |

Expand

Show lessSee more

**UNION ALL Operator:**

| c |
| --- |
| 3 |
| 1 |
| 2 |
| 2 |
| 3 |
| 4 |
| 5 |
| 1 |
| 1 |
| 2 |

Expand

Show lessSee more

### Known Issues

No related EWIs

### Related EWIs

- MSC-S000#: A SET operator with the ALL keyword is converted into a JOIN operation.
