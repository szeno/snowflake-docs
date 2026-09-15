# Code Conversion - Redshift Functional Differences

## SSC-FDM-RS0001

Data storage option is not supported in Snowflake. Data distribution is automatically handled by Snowflake.

### Description

In Snowflake, it is not necessary to explicitly define `SORTKEY` and `DISTSTYLE` when migrating from Redshift because Snowflake’s architecture inherently manages data distribution and optimization. Snowflake automatically handles data partitioning and indexing, optimizing query performance without requiring manual configuration of these parameters.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE table1 (
    col1 INTEGER
)
DISTSTYLE AUTO;

CREATE TABLE table2 (
    col1 INTEGER
)
SORTKEY AUTO;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE TABLE table1 (
    col1 INTEGER
)
----** SSC-FDM-RS0001 - DISTSTYLE AUTO OPTION IS NOT SUPPORTED IN SNOWFLAKE. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--DISTSTYLE AUTO
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';

CREATE TABLE table2 (
    col1 INTEGER
)
----** SSC-FDM-RS0001 - SORTKEY AUTO OPTION IS NOT SUPPORTED IN SNOWFLAKE. DATA STORAGE IS AUTOMATICALLY HANDLED BY SNOWFLAKE. **
--SORTKEY AUTO
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';
```

#### Best Practices

- It is advisable to assess the use of `CLUSTER BY` in Snowflake during migration from Redshift, as it may improve query performance by optimizing data locality for frequently queried columns.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-RS0002

The performance of CLUSTER BY in Snowflake may vary compared to the performance of SORTKEY in Redshift.

### Description

The `SORTKEY` (excluding `SORTKEY AUTO`) in Amazon Redshift are analogous to `CLUSTER BY` in Snowflake. However, performance implications may vary due to architectural differences between Redshift and Snowflake.

- **`SORTKEY`** improves performance by maintaining data in a sorted order based on specified columns. This is particularly beneficial for range queries and ordering operations.
- **`CLUSTER BY`** in Snowflake organizes data into blocks based on designated columns, aiding in filtering and aggregation tasks. However, it is less stringent about ordering compared to `SORTKEY`.

Understanding these mechanisms is crucial for optimizing performance in each respective platform.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE table1 (
    col1 INTEGER
)
SORTKEY (col1);

CREATE TABLE table2 (
    col1 INTEGER SORTKEY
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE TABLE table1 (
    col1 INTEGER
)
--** SSC-FDM-RS0002 - THE PERFORMANCE OF CLUSTER BY IN SNOWFLAKE MAY VARY COMPARED TO THE PERFORMANCE OF SORTKEY IN REDSHIFT **
CLUSTER BY (col1)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}'
;

CREATE TABLE table2 (
    col1 INTEGER
)
--** SSC-FDM-RS0002 - THE PERFORMANCE OF CLUSTER BY IN SNOWFLAKE MAY VARY COMPARED TO THE PERFORMANCE OF SORTKEY IN REDSHIFT **
CLUSTER BY (col1)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/17/2024" }}';
```

#### Best Practices

- **Benchmark after migration:** Run representative queries on both platforms to compare performance, as `CLUSTER BY` uses micro-partitioning rather than physical sort order.
- **Consider automatic clustering:** For large tables with frequent queries on specific columns, enable [automatic clustering](/user-guide/tables-auto-reclustering) in Snowflake.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-RS0003

Pending translation for Redshift foreign key constraints.

### Description

Pending translation for Redshift foreign key constraints. Snowflake supports [foreign key constraints](/sql-reference/constraints-overview), but they are not enforced and serve only as referential integrity metadata. This is a tool limitation, not a Snowflake platform limitation.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE TABLE1 (
    id INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE TABLE2 (
	id INTEGER,
	id_table1 INTEGER,
	FOREIGN KEY (id_table1) REFERENCES TABLE1 (col1)
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE TABLE TABLE1 (
    id INTEGER,
    PRIMARY KEY (id)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/26/2024" }}';

CREATE TABLE TABLE2 (
	id INTEGER,
	id_table1 INTEGER
--	                 ,
--    --** SSC-FDM-RS0003 - PENDING SNOWCONVERT AI TRANSLATION FOR REDSHIFT FOREIGN KEY CONSTRAINTS. **
--	FOREIGN KEY (id_table1) REFERENCES TABLE1 (col1)
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "09/26/2024" }}';
```

#### Best Practices

- You can manually [alter tables](https://docs.snowflake.com/en/sql-reference/sql/alter-table) with Foreign Keys and add them.

Copy code

```
 ALTER TABLE TABLE2 ADD CONSTRAINT
FOREIGN KEY (id_table1) REFERENCES TABLE1 (col1)
```

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-RS0004

It is possible that the date is wrong and Snowflake does not accept wrong dates

### Description

In Snowflake, using `TO_DATE` with an invalid date string (like ’20010631’) results in an error because it enforces strict validation, rejecting any non-existent dates. In contrast, Redshift’s `TO_DATE` can adjust such invalid dates to the nearest valid date (e.g., rolling June 31 to July 1) if the `is_strict` parameter is set to false. This difference highlights how Snowflake prioritizes data integrity by not automatically correcting invalid dates, while Redshift allows for more flexibility in date handling.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 SELECT TO_DATE('20010631', 'YYYYMMDD', FALSE);
```

##### Generated Code:

##### Snowflake

Copy code

```
 SELECT
TRY_TO_DATE(/*** SSC-FDM-RS0004 - INVALID DATES WILL CAUSE ERRORS IN SNOWFLAKE ***/ '20010631', 'YYYYMMDD');
```

#### Best Practices

- Check that the date is valid in the TRY\_TO\_DATE().
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-RS0005

Redshift MERGE rejects duplicate source rows. Snowflake allows them, which may produce different results.

### Description

In Redshift, the `MERGE` statement throws an error when the source table contains duplicate rows matching the join condition. Snowflake allows `MERGE` to execute with duplicate source rows, which may produce non-deterministic results when multiple source rows match the same target row.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN DELETE
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

##### Generated Code:

##### Snowflake

Copy code

```
 --** SSC-FDM-RS0005 - REDSHIFT MERGE STATEMENT REJECTS DUPLICATE SOURCE ROWS. SNOWFLAKE ALLOWS DUPLICATES, WHICH MAY PRODUCE NON-DETERMINISTIC RESULTS. **
MERGE INTO target USING source ON target.id = source.id
WHEN MATCHED THEN DELETE
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.name);
```

#### Best Practices

- **Deduplicate source data:** Add a `QUALIFY ROW_NUMBER() OVER (PARTITION BY join_key ORDER BY ...) = 1` to the source subquery to ensure each target row matches at most one source row.
- **Validate results:** After migration, compare `MERGE` output row counts between Redshift and Snowflake to detect non-deterministic behavior.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-RS0006

Called procedure contains usages of COMMIT/ROLLBACK. Modifying the current transaction in child scopes is not supported in Snowflake.

### Description

In Redshift, it is allowed to use the statements COMMIT and ROLLBACK inside a procedure to make permanent or discard the changes on a transaction that was opened on an outer scope.

Snowflake works with the concept of [scoped transactions](https://docs.snowflake.com/en/sql-reference/transactions#scoped-transactions), which treats each procedure call as a separate transaction, this limits the effects of the COMMIT and ROLLBACK statements to the scope of the procedure they are declared in.

The aforementioned functional difference will be warned with this FDM when calls to a procedure with COMMIT or ROLLBACK are detected by SnowConvert.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE inner_transaction_procedure(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    ROLLBACK;
    INSERT INTO transaction_values_test values (a + 1);
END
$$;

CREATE OR REPLACE PROCEDURE outer_transaction_procedure(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- This insert is also affected by the ROLLBACK in inner_transaction_procedure
    INSERT INTO transaction_values_test values (a);
    CALL inner_transaction_procedure(a + 3);
    COMMIT;
END
$$;

CALL outer_transaction_procedure(10);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE inner_transaction_procedure (a int)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a);
    ROLLBACK;
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a + 1);
    COMMIT;
END
$$;

CREATE OR REPLACE PROCEDURE outer_transaction_procedure (a int)
RETURNS VARCHAR
    LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    -- This insert is also affected by the ROLLBACK in inner_transaction_procedure
    INSERT INTO transaction_values_test
    values (:a);
    --** SSC-FDM-RS0006 - CALLED PROCEDURE CONTAINS USAGES OF COMMIT/ROLLBACK. MODIFYING THE CURRENT TRANSACTION IN CHILD SCOPES IS NOT SUPPORTED IN SNOWFLAKE **
    CALL inner_transaction_procedure(:a + 3);
    COMMIT;
END
$$;

CALL outer_transaction_procedure(10);
```

#### Best Practices

- **Refactor transaction control:** Move `COMMIT` and `ROLLBACK` statements into the outermost procedure or use [scoped transactions](/sql-reference/transactions) where supported.
- **Use caller’s rights:** Ensure the calling procedure manages the transaction boundary, as Snowflake’s scoped transactions isolate child procedure changes.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-RS0007

DDL statements perform an automatic COMMIT in Snowflake. ROLLBACK will not undo DDL-committed changes.

### Description

In Snowflake, [DDL statements perform an automatic commit](https://docs.snowflake.com/en/sql-reference/transactions#ddl) after their execution, making permanent all the changes in the current transaction, meaning they can not be discarded by a ROLLBACK.

When a ROLLBACK statement is found in a procedure that also contains a DDL statement, this FDM will be generated to inform about the DDL autocommit behavior.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE rollback_ddl(a int)
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO transaction_values_test values (a);
    CREATE TABLE someRollbackTable
    (
        col1 INTEGER
    );

    INSERT INTO someRollbackTable values (a);
    ROLLBACK;
END
$$;

CALL rollback_ddl(10);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE rollback_ddl (a int)
RETURNS VARCHAR
    LANGUAGE SQL
    COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "03/03/2025",  "domain": "test" }}'
    AS $$
BEGIN
    BEGIN TRANSACTION;
    INSERT INTO transaction_values_test
    values (:a);
    CREATE TABLE someRollbackTable
    (
        col1 INTEGER
    );
    BEGIN TRANSACTION;
    INSERT INTO someRollbackTable
    values (:a);
    --** SSC-FDM-RS0007 - DDL STATEMENTS PERFORM AN AUTOMATIC COMMIT IN SNOWFLAKE. ROLLBACK WILL NOT UNDO DDL-COMMITTED CHANGES **
    ROLLBACK;
END
$$;

CALL rollback_ddl(10);
```

#### Best Practices

- **Separate DDL from DML transactions:** Move DDL statements outside the transaction block, or execute them before `BEGIN TRANSACTION` to avoid implicit commits affecting DML operations.
- **Use conditional logic:** If DDL creation is conditional, check for object existence with `IF NOT EXISTS` to avoid unnecessary autocommits.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-RS0008

Snowflake uses autocommit by default. The NONATOMIC option is not supported in Snowflake.

### Description

In Redshift, the `NONATOMIC` option on `CREATE PROCEDURE` allows individual statements within the procedure to commit independently. In Snowflake, [autocommit](/sql-reference/transactions) is the default behavior — each statement is automatically committed unless wrapped in an explicit `BEGIN TRANSACTION` block. The `NONATOMIC` keyword is removed during migration because Snowflake’s autocommit provides equivalent semantics.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 CREATE OR REPLACE PROCEDURE SP_NONATOMIC()
NONATOMIC
AS
$$
    BEGIN
        NULL;
    END;
$$
LANGUAGE plpgsql;
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE SP_NONATOMIC ()
RETURNS VARCHAR
----** SSC-FDM-RS0008 - SNOWFLAKE USES AUTOCOMMIT BY DEFAULT. THE NONATOMIC OPTION IS NOT SUPPORTED IN SNOWFLAKE. **
--NONATOMIC
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "redshift",  "convertedOn": "02/10/2025",  "domain": "test" }}'
AS
$$
    BEGIN
        NULL;
    END;
$$;
```

#### Best Practices

- **Verify transaction behavior:** If the original Redshift procedure relied on `NONATOMIC` for partial commits, test the migrated Snowflake procedure to confirm that autocommit provides the expected semantics.
- **Add explicit transactions where needed:** If you need atomic (all-or-nothing) behavior for a group of statements in Snowflake, wrap them in `BEGIN TRANSACTION` … `COMMIT`.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-FDM-RS0009

DATEADD over a leap day with a non-constant year may differ from Redshift

#### Description

When the year quantity is not a compile-time constant, SnowConvert AI cannot determine whether adding it to February 29 produces a leap-year target. The generated `DATEADD` is left unchanged and this FDM is added because Redshift and Snowflake can resolve non-leap target years differently.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
SELECT DATEADD(year, col1, '2024-02-29');
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
DATEADD(year, col1, '2024-02-29') /*** SSC-FDM-RS0009 - DATEADD OVER A FEB-29 DATE WITH A NON-CONSTANT YEAR QUANTITY MAY DIFFER FROM REDSHIFT FOR NON-LEAP TARGET YEARS. ***/;
```

#### Best Practices

- Test leap-day inputs with non-constant year quantities and define the required behavior for non-leap target years.
- Add explicit date-adjustment logic when Snowflake’s result differs from the source requirement.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
