description:
:   Is this about the zipper merge in traffic?

# Snowpark Migration Accelerator: Merge

## Description

The `MERGE` statement combines data from one or more source tables with a target table, allowing you to perform updates and inserts in a single operation. Based on conditions you define, it determines whether to update existing rows or insert new ones in the target table. This makes it more efficient than using separate `INSERT`, `UPDATE`, and `DELETE` statements. The `MERGE` statement always produces consistent results when run multiple times with the same data.

In Spark, you can find the MERGE syntax in the [Spark documentation](https://docs.databricks.com/en/sql/language-manual/delta-merge-into.html).

Copy code

```
MERGE INTO target_table_name [target_alias]
   USING source_table_reference [source_alias]
   ON merge_condition
   { WHEN MATCHED [ AND matched_condition ] THEN matched_action |
     WHEN NOT MATCHED [BY TARGET] [ AND not_matched_condition ] THEN not_matched_action |
     WHEN NOT MATCHED BY SOURCE [ AND not_matched_by_source_condition ] THEN not_matched_by_source_action } [...]

matched_action
 { DELETE |
   UPDATE SET * |
   UPDATE SET { column = { expr | DEFAULT } } [, ...] }

not_matched_action
 { INSERT * |
   INSERT (column1 [, ...] ) VALUES ( expr | DEFAULT ] [, ...] )

not_matched_by_source_action
 { DELETE |
   UPDATE SET { column = { expr | DEFAULT } } [, ...] }
```

In Snowflake, the MERGE statement follows this syntax (For additional details, refer to the [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/sql/merge)):

Copy code

```
MERGE INTO <target_table> USING <source> ON <join_expr> { matchedClause | notMatchedClause } [ ... ]

matchedClause ::=
  WHEN MATCHED [ AND <case_predicate> ] THEN { UPDATE SET <col_name> = <expr> [ , <col_name2> = <expr2> ... ] | DELETE } [ ... ]

notMatchedClause ::=
   WHEN NOT MATCHED [ AND <case_predicate> ] THEN INSERT [ ( <col_name> [ , ... ] ) ] VALUES ( <expr> [ , ... ] )
```

The key distinction is that Snowflake lacks a direct equivalent to the `WHEN NOT MATCHED BY SOURCE` clause. A workaround solution is required to achieve similar functionality in Snowflake.

## Sample Source Patterns

### Sample auxiliary data

Note

The following code examples have been executed to help you better understand how they work:

Copy code

```
CREATE OR REPLACE people_source (
  person_id  INTEGER NOT NULL PRIMARY KEY,
  first_name STRING NOT NULL,
  last_name  STRING NOT NULL,
  title      STRING NOT NULL,
);

CREATE OR REPLACE TABLE people_target (
  person_id  INTEGER NOT NULL PRIMARY KEY,
  first_name STRING NOT NULL,
  last_name  STRING NOT NULL,
  title      STRING NOT NULL DEFAULT 'NONE'
);

INSERT INTO people_target VALUES (1, 'John', 'Smith', 'Mr');
INSERT INTO people_target VALUES (2, 'alice', 'jones', 'Mrs');
INSERT INTO people_source VALUES (2, 'Alice', 'Jones', 'Mrs.');
INSERT INTO people_source VALUES (3, 'Jane', 'Doe', 'Miss');
INSERT INTO people_source VALUES (4, 'Dave', 'Brown', 'Mr');
```

Copy code

```
CREATE OR REPLACE TABLE people_source (
    person_id  INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    title VARCHAR(10) NOT NULL
);

CREATE OR REPLACE TABLE people_target (
    person_id  INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    title VARCHAR(10) NOT NULL DEFAULT 'NONE'
);

INSERT INTO people_target VALUES (1, 'John', 'Smith', 'Mr');
INSERT INTO people_target VALUES (2, 'alice', 'jones', 'Mrs');
INSERT INTO people_source VALUES (2, 'Alice', 'Jones', 'Mrs.');
INSERT INTO people_source VALUES (3, 'Jane', 'Doe', 'Miss');
INSERT INTO people_source VALUES (4, 'Dave', 'Brown', 'Mr');
```

### MERGE Statement - Insert and Update Case

#### Spark

Copy code

```
MERGE INTO people_target pt
USING people_source ps
ON    (pt.person_id = ps.person_id)
WHEN MATCHED THEN UPDATE
  SET pt.first_name = ps.first_name,
      pt.last_name = ps.last_name,
      pt.title = DEFAULT
WHEN NOT MATCHED THEN INSERT
  (pt.person_id, pt.first_name, pt.last_name, pt.title)
  VALUES (ps.person_id, ps.first_name, ps.last_name, ps.title);

SELECT * FROM people_target;
```

```
PERSON_ID%FIRST_NAME%LAST_NAME%TITLE%
---------+----------+---------+-----+
        1|John      |Smith    |Mr   |
        2|Alice     |Jones    |NONE |
        3|Jane      |Doe      |Miss |
        4|Dave      |Brown    |Mr   |
```

#### Snowflake

Copy code

```
MERGE INTO people_target2 pt
USING people_source ps
ON    (pt.person_id = ps.person_id)
WHEN MATCHED THEN UPDATE
  SET pt.first_name = ps.first_name,
      pt.last_name = ps.last_name,
      pt.title = DEFAULT
WHEN NOT MATCHED THEN INSERT
  (pt.person_id, pt.first_name, pt.last_name, pt.title)
  VALUES (ps.person_id, ps.first_name, ps.last_name, ps.title);

SELECT * FROM PUBLIC.people_target ORDER BY person_id;
```

```
PERSON_ID%FIRST_NAME%LAST_NAME%TITLE%
---------+----------+---------+-----+
        1|John      |Smith    |Mr   |
        2|Alice     |Jones    |NONE |
        3|Jane      |Doe      |Miss |
        4|Dave      |Brown    |Mr   |
```

The `INSERT` and `UPDATE` operations work the same way in Snowflake. In both SQL dialects, you can use `DEFAULT` as an expression to set a column to its default value.

Spark allows insert and update operations without explicitly listing the columns. When columns are not specified, the operation affects all columns in the table. For this to work correctly, the source and destination tables must have identical column structures. If the column structures don’t match, you will receive a parsing error.

Copy code

```
UPDATE SET *
-- This is equivalent to UPDATE SET col1 = source.col1 [, col2 = source.col2 ...]

INSERT *
-- This command copies all columns from the source table to the target table, matching columns by name. It is the same as explicitly listing all columns in both the INSERT and VALUES clauses.

Since Snowflake doesn't support these options, the migration process will instead list all columns from the target table.

### MERGE Statement - Delete Case

```{code} sql
:force:
MERGE INTO people_target pt
USING people_source ps
ON    (pt.person_id = ps.person_id)
WHEN MATCHED AND pt.person_id &lt; 3 THEN DELETE
WHEN NOT MATCHED BY TARGET THEN INSERT *;

SELECT * FROM people_target;
```

```
PERSON_ID%FIRST_NAME%LAST_NAME%TITLE%
---------+----------+---------+-----+
        1|John      |Smith    |Mr   |
        3|Jane      |Doe      |Miss |
        4|Dave      |Brown    |Mr   |
```

#### Snowflake

Copy code

```
MERGE INTO people_target pt
USING people_source ps
ON    (pt.person_id = ps.person_id)
WHEN MATCHED AND pt.person_id &lt; 3 THEN DELETE
WHEN NOT MATCHED THEN INSERT
  (pt.person_id, pt.first_name, pt.last_name, pt.title)
  VALUES (ps.person_id, ps.first_name, ps.last_name, ps.title);

SELECT * FROM people_target;
```

```
PERSON_ID%FIRST_NAME%LAST_NAME%TITLE%
---------+----------+---------+-----+
        1|John      |Smith    |Mr   |
        3|Jane      |Doe      |Miss |
        4|Dave      |Brown    |Mr   |
```

The `DELETE` action in Snowflake works the same way as in other databases. You can also add additional conditions to the `MATCHED` and `NOT MATCHED` clauses.

`WHEN NOT MATCHED BY TARGET` and `WHEN NOT MATCHED` are equivalent clauses that can be used interchangeably in SQL merge statements.

### MERGE Statement - WHEN NOT MATCHED BY SOURCE

`WHEN NOT MATCHED BY SOURCE` clauses are triggered when a row in the target table has no matching rows in the source table. This occurs when both the `merge_condition` and the optional `not_match_by_source_condition` evaluate to true. For more details, see the [Spark documentation](https://docs.databricks.com/en/sql/language-manual/delta-merge-into.html).

Snowflake does not support this clause directly. To handle this limitation, you can use the following workaround for both `DELETE` and `UPDATE` actions.

Copy code

```
MERGE INTO people_target pt
USING people_source ps
ON pt.person_id = ps.person_id
WHEN NOT MATCHED BY SOURCE THEN DELETE;

SELECT * FROM people_target;
```

```
PERSON_ID%FIRST_NAME%LAST_NAME%TITLE%
---------+----------+---------+-----+
        2|Alice     |Jones    |NONE |
```

#### Snowflake

Copy code

```
MERGE INTO people_target pt
USING (
    SELECT
        pt.person_id
    FROM
        people_target pt LEFT
    JOIN people_source ps ON pt.person_id = ps.person_id
    WHERE
        ps.person_id is null
) s_src
    ON s_src.person_id = pt.person_id
WHEN MATCHED THEN DELETE;

SELECT * FROM people_target;
```

```
PERSON_ID%FIRST_NAME%LAST_NAME%TITLE%
---------+----------+---------+-----+
        2|Alice     |Jones    |NONE |
```

The `DELETE` action in Snowflake works the same way as in other databases. You can also add additional conditions to the `MATCHED` and `NOT MATCHED` clauses.

## Known issues

### 1. MERGE is very similar in both languages

While Apache Spark offers additional features, you can achieve similar functionality in Snowflake using alternative approaches, as demonstrated in the previous examples.

## Related EWIs

No related Errors, Warnings, and Issues (EWIs) found.
