description:
:   Oh where has my translation reference gone?

# Snowpark Migration Accelerator: Where

## Description

Filters the data returned by a query or subquery based on specified conditions. ([Databricks SQL Language Reference WHERE](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-qry-select-where.html))

The `WHERE` clause filters data by defining specific conditions that must be met. ([Snowflake SQL Language Reference WHERE](https://docs.snowflake.com/en/sql-reference/constructs/where))

### Syntax

Copy code

```
WHERE <boolean_expression>
```

Copy code

```
...
WHERE <predicate>
[ ... ]
```

## Sample Source Patterns

### Setup data

#### Databricks

Copy code

```
CREATE TABLE person (id INT, name STRING, age INT);
INSERT INTO person VALUES
    (100, 'John',   30),
    (200, 'Mary', NULL),
    (300, 'Mike',   80),
    (400, 'Dan' ,   50);
```

#### Snowflake

Copy code

```
 CREATE TABLE person (id INT, name STRING, age INT);
 INSERT INTO person VALUES
    (100, 'John',   30),
    (200, 'Mary', NULL),
    (300, 'Mike',   80),
    (400, 'Dan' ,   50);
```

### Pattern code

#### Databricks

Copy code

```
-- 1. Comparison operator in `WHERE` clause.
SELECT * FROM person WHERE id > 200 ORDER BY id;

-- 2. Comparison and logical operators in `WHERE` clause.
SELECT * FROM person WHERE id = 200 OR id = 300 ORDER BY id;

-- 3. IS NULL expression in `WHERE` clause.
SELECT * FROM person WHERE id > 300 OR age IS NULL ORDER BY id;

-- 4. Function expression in `WHERE` clause.
SELECT * FROM person WHERE length(name) > 3 ORDER BY id;

-- 5. `BETWEEN` expression in `WHERE` clause.
SELECT * FROM person WHERE id BETWEEN 200 AND 300 ORDER BY id;

-- 6. Scalar Subquery in `WHERE` clause.
SELECT * FROM person WHERE age > (SELECT avg(age) FROM person);

-- 7. Correlated Subquery in `WHERE` clause.
SELECT * FROM person AS parent
   WHERE EXISTS (SELECT 1 FROM person AS child
                  WHERE parent.id = child.id
                    AND child.age IS NULL);
```

1. Use comparison operators (such as =, >, <, >=, <=) in the `WHERE` clause to filter data.

| ID | NAME | AGE |
| --- | --- | --- |
| 300 | Mike | 80 |
| 400 | Dan | 50 |

Expand

Show lessSee more

---

1. Use comparison operators (=, <, >, <=, >=, !=) and logical operators (AND, OR, NOT) in the `WHERE` clause to filter data.

| ID | NAME | AGE |
| --- | --- | --- |
| 200 | Mary | null |
| 300 | Mike | 80 |

Expand

Show lessSee more

---

1. Using `IS NULL` in the `WHERE` clause to check for null values.

| ID | NAME | AGE |
| --- | --- | --- |
| 200 | Mary | null |
| 400 | Dan | 50 |

Expand

Show lessSee more

---

1. Using function expressions within a `WHERE` clause.

| ID | NAME | AGE |
| --- | --- | --- |
| 100 | John | 30 |
| 200 | Mary | null |
| 300 | Mike | 80 |

Expand

Show lessSee more

---

1. Using the `BETWEEN` operator in a `WHERE` clause to filter data based on a range of values.

| ID | NAME | AGE |
| --- | --- | --- |
| 200 | Mary | null |
| 300 | Mike | 80 |

Expand

Show lessSee more

---

1. Using a Scalar Subquery within a `WHERE` clause.

| ID | NAME | AGE |
| --- | --- | --- |
| 300 | Mike | 80 |

Expand

Show lessSee more

---

1. A subquery in the `WHERE` clause that references columns from the outer query.

| ID | NAME | AGE |
| --- | --- | --- |
| 200 | Mary | null |

Expand

Show lessSee more

#### Snowflake

Copy code

```
-- 1. Comparison operator in `WHERE` clause.
SELECT * FROM person WHERE id > 200 ORDER BY id;

-- 2. Comparison and logical operators in `WHERE` clause.
SELECT * FROM person WHERE id = 200 OR id = 300 ORDER BY id;

-- 3. IS NULL expression in `WHERE` clause.
SELECT * FROM person WHERE id > 300 OR age IS NULL ORDER BY id;

-- 4. Function expression in `WHERE` clause.
SELECT * FROM person WHERE length(name) > 3 ORDER BY id;

-- 5. `BETWEEN` expression in `WHERE` clause.
SELECT * FROM person WHERE id BETWEEN 200 AND 300 ORDER BY id;

-- 6. Scalar Subquery in `WHERE` clause.
SELECT * FROM person WHERE age > (SELECT avg(age) FROM person);

-- 7. Correlated Subquery in `WHERE` clause.
SELECT * FROM person AS parent
   WHERE EXISTS (SELECT 1 FROM person AS child
                  WHERE parent.id = child.id
                    AND child.age IS NULL);
```

1. Use comparison operators (such as =, >, <, >=, <=) in the `WHERE` clause to filter data.

| ID | NAME | AGE |
| --- | --- | --- |
| 300 | Mike | 80 |
| 400 | Dan | 50 |

Expand

Show lessSee more

---

1. Using comparison operators (such as =, <, >, <=, >=) and logical operators (such as AND, OR, NOT) in the `WHERE` clause to filter data.

| ID | NAME | AGE |
| --- | --- | --- |
| 200 | Mary | null |
| 300 | Mike | 80 |

Expand

Show lessSee more

---

1. Using `IS NULL` in the `WHERE` clause to check for null values.

| ID | NAME | AGE |
| --- | --- | --- |
| 200 | Mary | null |
| 400 | Dan | 50 |

Expand

Show lessSee more

---

1. Using function expressions within a `WHERE` clause.

| ID | NAME | AGE |
| --- | --- | --- |
| 100 | John | 30 |
| 200 | Mary | null |
| 300 | Mike | 80 |

Expand

Show lessSee more

---

1. Using the `BETWEEN` operator in a `WHERE` clause to filter data based on a range of values.

| ID | NAME | AGE |
| --- | --- | --- |
| 200 | Mary | null |
| 300 | Mike | 80 |

Expand

Show lessSee more

---

1. Using a Scalar Subquery within a `WHERE` clause.

| ID | NAME | AGE |
| --- | --- | --- |
| 300 | Mike | 80 |

Expand

Show lessSee more

---

1. Correlated Subquery in `WHERE` clause.

| ID | NAME | AGE |
| --- | --- | --- |
| 200 | Mary | null |

Expand

Show lessSee more

### Known Issues

No issues were found

### Related EWIs

No related EWIs
