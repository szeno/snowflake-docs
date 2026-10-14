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

## SSC-FDM-RS0010

The Redshift S3 credentials cannot be translated.

#### Description

SnowConvert AI reports SSC-FDM-RS0010 while converting Redshift code because the Snowflake result is not the same as the source. The Redshift s3 credentials cannot be translated. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
COPY copy_csv_t1 FROM 's3://bucket/key' IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-role' FORMAT AS CSV;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-RS0010 - REDSHIFT S3 CREDENTIALS HAVE NO SNOWFLAKE COUNTERPART. CREATE A STORAGE INTEGRATION NAMED 'bucket_integration' WITH ACCESS TO 's3://bucket/key' AND GRANT USAGE ON IT BEFORE RUNNING THE GENERATED COPY INTO. **
COPY INTO copy_csv_t1
FROM 's3://bucket/key'
STORAGE_INTEGRATION = bucket_integration
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"');
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0010 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0011

PARALLEL OFF was translated to SINGLE = TRUE.

#### Description

SnowConvert AI reports SSC-FDM-RS0011 while converting Redshift code because the Snowflake result is not the same as the source. Redshift parallel off was translated to single = true. Snowflake writes one file and fails when it exceeds the maximum file size instead of splitting it as Redshift does. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
UNLOAD ('SELECT id FROM sales.orders')
TO 's3://company-exports/single/'
IAM_ROLE DEFAULT
CSV
PARALLEL OFF;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-RS0010 - REDSHIFT S3 CREDENTIALS HAVE NO SNOWFLAKE COUNTERPART. CREATE A STORAGE INTEGRATION NAMED 'company_exports_integration' WITH ACCESS TO 's3://company-exports/single/' AND GRANT USAGE ON IT BEFORE RUNNING THE GENERATED COPY INTO. **
--** SSC-FDM-RS0011 - REDSHIFT PARALLEL OFF WAS TRANSLATED TO SINGLE = TRUE. SNOWFLAKE WRITES ONE FILE AND FAILS WHEN IT EXCEEDS THE MAXIMUM FILE SIZE INSTEAD OF SPLITTING IT AS REDSHIFT DOES. **
COPY INTO 's3://company-exports/single/'
FROM
(
SELECT
id
FROM
sales.orders
)
STORAGE_INTEGRATION = company_exports_integration
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"')
SINGLE = TRUE;
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0011 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0012

Partition columns stay in the unloaded data.

#### Description

SnowConvert AI reports SSC-FDM-RS0012 while converting Redshift code because the Snowflake result is not the same as the source. Redshift omits the partition columns from the unloaded files unless ‘include’ is used. The generated Snowflake partition by expression always keeps them in the projected data. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
UNLOAD ('SELECT id, Year FROM sales.orders')
TO 's3://company-exports/folded/'
IAM_ROLE DEFAULT
CSV
PARTITION BY (Year);
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-RS0010 - REDSHIFT S3 CREDENTIALS HAVE NO SNOWFLAKE COUNTERPART. CREATE A STORAGE INTEGRATION NAMED 'company_exports_integration' WITH ACCESS TO 's3://company-exports/folded/' AND GRANT USAGE ON IT BEFORE RUNNING THE GENERATED COPY INTO. **
--** SSC-FDM-RS0012 - REDSHIFT OMITS THE PARTITION COLUMNS FROM THE UNLOADED FILES UNLESS 'INCLUDE' IS USED. THE GENERATED SNOWFLAKE PARTITION BY EXPRESSION ALWAYS KEEPS THEM IN THE PROJECTED DATA. **
COPY INTO 's3://company-exports/folded/'
FROM
(
SELECT
id,
Year
FROM
sales.orders
)
PARTITION BY CONCAT('year=', Year)
STORAGE_INTEGRATION = company_exports_integration
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"');
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0012 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0013

CASCADE was not carried over to the dynamic table refresh

#### Description

SnowConvert AI reports SSC-FDM-RS0013 while converting Redshift code because the Snowflake result is not the same as the source. Cascade was not carried over to the dynamic table refresh. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
REFRESH MATERIALIZED VIEW prod.vw_rpt_general_ledger CASCADE;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-RS0013 - THE CASCADE OPTION WAS NOT CARRIED OVER: REDSHIFT ALSO REFRESHES MATERIALIZED VIEWS DEPENDING ON 'prod.vw_rpt_general_ledger', WHILE SNOWFLAKE REFRESHES ONLY 'prod.vw_rpt_general_ledger', SO DEPENDENT DYNAMIC TABLES RELY ON THEIR OWN TARGET_LAG. **
ALTER DYNAMIC TABLE prod.vw_rpt_general_ledger REFRESH;
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0013 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0014

The RESTRICT keyword was removed; it is applied by default in Snowflake

#### Description

SnowConvert AI reports SSC-FDM-RS0014 while converting Redshift code because the Snowflake result is not the same as the source. The restrict keyword was removed, applied by default in Snowflake. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
REFRESH MATERIALIZED VIEW prod.vw_rpt_general_ledger RESTRICT;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-RS0014 - THE RESTRICT KEYWORD WAS REMOVED, APPLIED BY DEFAULT IN SNOWFLAKE. **
ALTER DYNAMIC TABLE prod.vw_rpt_general_ledger REFRESH;
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0014 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0015

The procedure name was renamed to a valid Snowflake identifier.

#### Description

SnowConvert AI reports SSC-FDM-RS0015 while converting Redshift code because the Snowflake result is not the same as the source. The procedure name was renamed to a valid Snowflake identifier. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
CREATE OR REPLACE PROCEDURE dev_staging."my-proc-name"() AS $$ BEGIN NULL; END; $$ LANGUAGE plpgsql;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE
--** SSC-FDM-RS0015 - PROCEDURE NAME 'dev_staging."my-proc-name"' IS NOT A VALID SNOWFLAKE IDENTIFIER UNQUOTED, SO IT WAS RENAMED TO 'dev_staging.my_proc_name'. UPDATE REFERENCES FROM CODE OUTSIDE THIS CONVERSION. **
dev_staging.my_proc_name ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS $$ BEGIN NULL; END; $$;
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0015 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0016

The procedure moved to a renamed schema while other objects did not.

#### Description

SnowConvert AI reports SSC-FDM-RS0016 while converting Redshift code because the Snowflake result is not the same as the source. The procedure moved to a renamed schema while other objects did not. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
CREATE OR REPLACE PROCEDURE "5_dev"."my-proc-name"() AS $$ BEGIN NULL; END; $$ LANGUAGE plpgsql;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE
--** SSC-FDM-RS0015 - PROCEDURE NAME '"5_dev"."my-proc-name"' IS NOT A VALID SNOWFLAKE IDENTIFIER UNQUOTED, SO IT WAS RENAMED TO '_5_dev.my_proc_name'. UPDATE REFERENCES FROM CODE OUTSIDE THIS CONVERSION. **
--** SSC-FDM-RS0016 - THE SCHEMA QUALIFIER OF THIS PROCEDURE WAS RENAMED FROM '"5_dev"' TO '_5_dev'. TABLES AND VIEWS DECLARED IN '"5_dev"' ARE NOT RENAMED BY THIS CONVERSION, SO THE PROCEDURE NOW LIVES IN A DIFFERENT SCHEMA THAN THE OBJECTS ITS BODY REFERENCES WITHOUT A QUALIFIER. **
_5_dev.my_proc_name ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS $$ BEGIN NULL; END; $$;
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0016 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0017

MAXERROR has no COPY INTO counterpart, so the load now aborts on the first bad row.

#### Description

SnowConvert AI reports SSC-FDM-RS0017 while converting Redshift code because the Snowflake result is not the same as the source. Maxerror has no copy into counterpart, so the load now aborts on the first bad row. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
COPY t1 FROM 's3://bucket/key' IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-role' FORMAT AS CSV MAXERROR 100;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-RS0010 - REDSHIFT S3 CREDENTIALS HAVE NO SNOWFLAKE COUNTERPART. CREATE A STORAGE INTEGRATION NAMED 'bucket_integration' WITH ACCESS TO 's3://bucket/key' AND GRANT USAGE ON IT BEFORE RUNNING THE GENERATED COPY INTO. **
--** SSC-FDM-RS0017 - REDSHIFT 'MAXERROR 100' LET THE LOAD CONTINUE UNTIL THAT MANY ROWS HAD FAILED. SNOWFLAKE HAS NO EQUIVALENT COUNT, SO THE GENERATED COPY INTO KEEPS THE DEFAULT ON_ERROR = ABORT_STATEMENT AND STOPS AT THE FIRST BAD ROW. **
COPY INTO t1
FROM 's3://bucket/key'
STORAGE_INTEGRATION = bucket_integration
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"');
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0017 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0018

Redshift CONVERT to TIMESTAMP may interpret digit-only strings differently in Snowflake.

#### Description

SnowConvert AI reports SSC-FDM-RS0018 while converting Redshift code because the Snowflake result is not the same as the source. Redshift convert to timestamp reads digit-only strings as calendar dates. Snowflake cast may read them as unix epoch offsets. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
SELECT CONVERT(timestamp, '20240115') AS r;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  CAST('20240115' AS TIMESTAMP) /*** SSC-FDM-RS0018 - REDSHIFT CONVERT TO TIMESTAMP READS DIGIT-ONLY STRINGS AS CALENDAR DATES. SNOWFLAKE CAST MAY READ THEM AS UNIX EPOCH OFFSETS. ***/ AS r;
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0018 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0019

Redshift REAL uses single precision while Snowflake REAL uses double precision.

#### Description

SnowConvert AI reports SSC-FDM-RS0019 while converting Redshift code because the Snowflake result is not the same as the source. Redshift real uses single precision. Snowflake real uses double precision, so values may differ. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
SELECT CONVERT(real, '3.14') AS r;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  CAST('3.14' AS REAL) /*** SSC-FDM-RS0019 - REDSHIFT REAL USES SINGLE PRECISION. SNOWFLAKE REAL USES DOUBLE PRECISION, SO VALUES MAY DIFFER. ***/ AS r;
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0019 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0020

Redshift TEXT\_TO\_NUMERIC\_ALT converts an empty string to zero while Snowflake TRY\_TO\_NUMBER returns NULL.

#### Description

SnowConvert AI reports SSC-FDM-RS0020 while converting Redshift code because the Snowflake result is not the same as the source. Redshift TEXT\_TO\_NUMERIC\_ALT converts an empty string to zero. Snowflake TRY\_TO\_NUMBER returns null for the same input. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
SELECT text_to_numeric_alt('', 10, 2) AS parsed_value;
```

##### Output Code:

##### Snowflake

Copy code

```
SELECT
  TRY_TO_NUMBER('', 10, 2) /*** SSC-FDM-RS0020 - REDSHIFT TEXT_TO_NUMERIC_ALT CONVERTS AN EMPTY STRING TO ZERO. SNOWFLAKE TRY_TO_NUMBER RETURNS NULL FOR THE SAME INPUT. ***/ AS parsed_value;
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0020 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0021

OVERWRITE was removed because Snowflake rejects OVERWRITE beside PARTITION BY, and existing partition files are not overwritten.

#### Description

SnowConvert AI reports SSC-FDM-RS0021 while converting Redshift code because the Snowflake result is not the same as the source. Overwrite was removed because Snowflake rejects overwrite beside partition by (002328), and existing partition files are not overwritten the way Redshift allowoverwrite would. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
UNLOAD ('SELECT id, year FROM sales.orders')
TO 's3://company-exports/partover/'
IAM_ROLE DEFAULT
CSV
ALLOWOVERWRITE
PARTITION BY (year);
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-RS0010 - REDSHIFT S3 CREDENTIALS HAVE NO SNOWFLAKE COUNTERPART. CREATE A STORAGE INTEGRATION NAMED 'company_exports_integration' WITH ACCESS TO 's3://company-exports/partover/' AND GRANT USAGE ON IT BEFORE RUNNING THE GENERATED COPY INTO. **
--** SSC-FDM-RS0021 - OVERWRITE WAS REMOVED BECAUSE SNOWFLAKE REJECTS OVERWRITE BESIDE PARTITION BY (002328), AND EXISTING PARTITION FILES ARE NOT OVERWRITTEN THE WAY REDSHIFT ALLOWOVERWRITE WOULD. **
--** SSC-FDM-RS0012 - REDSHIFT OMITS THE PARTITION COLUMNS FROM THE UNLOADED FILES UNLESS 'INCLUDE' IS USED. THE GENERATED SNOWFLAKE PARTITION BY EXPRESSION ALWAYS KEEPS THEM IN THE PROJECTED DATA. **
COPY INTO 's3://company-exports/partover/'
FROM
(
SELECT
id,
year
FROM
sales.orders
)
PARTITION BY CONCAT('year=', year)
STORAGE_INTEGRATION = company_exports_integration
FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"');
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0021 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0022

REMOVEQUOTES was mapped to FIELD\_OPTIONALLY\_ENCLOSED\_BY, which parses the character as an optional enclosure instead of only stripping quotes.

#### Description

SnowConvert AI reports SSC-FDM-RS0022 while converting Redshift code because the Snowflake result is not the same as the source. FIELD\_OPTIONALLY\_ENCLOSED\_BY replaces removequotes. Redshift only strips the surrounding quotes, while Snowflake parses the character as an optional enclosure, including its escape rules. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
COPY t1 FROM 's3://bucket/key' IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-role' DELIMITER ',' REMOVEQUOTES;
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-RS0010 - REDSHIFT S3 CREDENTIALS HAVE NO SNOWFLAKE COUNTERPART. CREATE A STORAGE INTEGRATION NAMED 'bucket_integration' WITH ACCESS TO 's3://bucket/key' AND GRANT USAGE ON IT BEFORE RUNNING THE GENERATED COPY INTO. **
--** SSC-FDM-RS0022 - FIELD_OPTIONALLY_ENCLOSED_BY REPLACES REMOVEQUOTES. REDSHIFT ONLY STRIPS THE SURROUNDING QUOTES, WHILE SNOWFLAKE PARSES THE CHARACTER AS AN OPTIONAL ENCLOSURE, INCLUDING ITS ESCAPE RULES. **
COPY INTO t1
FROM 's3://bucket/key'
STORAGE_INTEGRATION = bucket_integration
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' FIELD_OPTIONALLY_ENCLOSED_BY = '"');
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0022 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0023

The COPY REGION option was removed because a Snowflake COPY INTO location does not take a region.

#### Description

SnowConvert AI reports SSC-FDM-RS0023 while converting Redshift code because the Snowflake result is not the same as the source. The copy region option was removed because a Snowflake copy into location does not take a region. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
COPY t1 FROM 's3://bucket/key' IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-role' REGION 'us-east-1' DELIMITER ',';
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-RS0010 - REDSHIFT S3 CREDENTIALS HAVE NO SNOWFLAKE COUNTERPART. CREATE A STORAGE INTEGRATION NAMED 'bucket_integration' WITH ACCESS TO 's3://bucket/key' AND GRANT USAGE ON IT BEFORE RUNNING THE GENERATED COPY INTO. **
--** SSC-FDM-RS0023 - REGION 'us-east-1' WAS REMOVED BECAUSE A SNOWFLAKE COPY INTO LOCATION DOES NOT TAKE A REGION. CONFIGURE THE REGION ON THE STORAGE INTEGRATION OR THE STAGE URL. **
COPY INTO t1
FROM 's3://bucket/key'
STORAGE_INTEGRATION = bucket_integration
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',');
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0023 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0024

FILE\_EXTENSION is ignored when SINGLE = TRUE.

#### Description

SnowConvert AI reports SSC-FDM-RS0024 while converting Redshift code because the Snowflake result is not the same as the source. Redshift extension was translated to FILE\_EXTENSION beside single = true. Snowflake ignores FILE\_EXTENSION when single = true, so the unloaded file does not receive that extension. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
UNLOAD ('SELECT id FROM sales.orders')
TO 's3://company-exports/csv/'
IAM_ROLE DEFAULT
CSV
HEADER
ALLOWOVERWRITE
PARALLEL OFF
EXTENSION 'csv';
```

##### Output Code:

##### Snowflake

Copy code

```
--** SSC-FDM-RS0010 - REDSHIFT S3 CREDENTIALS HAVE NO SNOWFLAKE COUNTERPART. CREATE A STORAGE INTEGRATION NAMED 'company_exports_integration' WITH ACCESS TO 's3://company-exports/csv/' AND GRANT USAGE ON IT BEFORE RUNNING THE GENERATED COPY INTO. **
--** SSC-FDM-RS0011 - REDSHIFT PARALLEL OFF WAS TRANSLATED TO SINGLE = TRUE. SNOWFLAKE WRITES ONE FILE AND FAILS WHEN IT EXCEEDS THE MAXIMUM FILE SIZE INSTEAD OF SPLITTING IT AS REDSHIFT DOES. **
--** SSC-FDM-RS0024 - REDSHIFT EXTENSION WAS TRANSLATED TO FILE_EXTENSION BESIDE SINGLE = TRUE. SNOWFLAKE IGNORES FILE_EXTENSION WHEN SINGLE = TRUE, SO THE UNLOADED FILE DOES NOT RECEIVE THAT EXTENSION. **
COPY INTO 's3://company-exports/csv/'
FROM
(
SELECT
id
FROM
sales.orders
)
STORAGE_INTEGRATION = company_exports_integration
FILE_FORMAT = (TYPE = CSV FILE_EXTENSION = 'csv' FIELD_OPTIONALLY_ENCLOSED_BY = '"')
HEADER = TRUE
OVERWRITE = TRUE
SINGLE = TRUE;
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0024 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0025

ON\_ERROR = CONTINUE skips a bad row instead of replacing the failed value.

#### Description

SnowConvert AI reports SSC-FDM-RS0025 while converting Redshift code because the Snowflake result is not the same as the source. Snowflake ON\_ERROR = continue skips a row containing a conversion error. Redshift ignoreallerrors keeps the row and replaces the failed value. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
CREATE OR REPLACE PROCEDURE ssc_scratch_copy_ignore_all_errors()
AS $$
BEGIN
  COPY t1 FROM 's3://bucket/key' IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-role' CSV IGNOREALLERRORS;
END;
$$ LANGUAGE plpgsql;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE OR REPLACE PROCEDURE ssc_scratch_copy_ignore_all_errors ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS $$
    BEGIN
      --** SSC-FDM-RS0010 - REDSHIFT S3 CREDENTIALS HAVE NO SNOWFLAKE COUNTERPART. CREATE A STORAGE INTEGRATION NAMED 'bucket_integration' WITH ACCESS TO 's3://bucket/key' AND GRANT USAGE ON IT BEFORE RUNNING THE GENERATED COPY INTO. **
      --** SSC-FDM-RS0025 - SNOWFLAKE ON_ERROR = CONTINUE SKIPS A ROW CONTAINING A CONVERSION ERROR. REDSHIFT IGNOREALLERRORS KEEPS THE ROW AND REPLACES THE FAILED VALUE. **
      COPY INTO t1
      FROM 's3://bucket/key'
      STORAGE_INTEGRATION = bucket_integration
      FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"')
      ON_ERROR = CONTINUE;
    END;
$$;
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0025 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0026

Redshift session configuration parameter has no Snowflake counterpart.

#### Description

SnowConvert AI reports SSC-FDM-RS0026 while converting Redshift code because the Snowflake result is not the same as the source. Redshift session configuration parameter has no Snowflake counterpart. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
CREATE PROCEDURE reset_parameter()
AS $$
BEGIN
  RESET enable_case_sensitive_identifier;
  INSERT INTO reset_log VALUES ('after reset');
END;
$$ LANGUAGE plpgsql;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE PROCEDURE reset_parameter ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
  $$
    BEGIN
--      --** SSC-FDM-RS0026 - SESSION CONFIGURATION PARAMETER 'enable_case_sensitive_identifier' HAS NO SNOWFLAKE COUNTERPART. THE STATEMENT WAS REMOVED. **
--      RESET enable_case_sensitive_identifier;
      INSERT INTO reset_log
      VALUES ('after reset');
    END;
  $$;
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0026 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.

## SSC-FDM-RS0029

Redshift truncates or rounds half to even when it casts a fractional value to an integer, while Snowflake rounds half away from zero.

#### Description

SnowConvert AI reports SSC-FDM-RS0029 while converting Redshift code because the Snowflake result is not the same as the source. Redshift truncates a fractional value from table rows and rounds a floating-point constant half to even when it casts the value to an integer type. Snowflake rounds half away from zero, so values may differ. The sample below is a verified conversion, and the Snowflake statement includes the marker the product emits.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
CREATE TABLE measures (f FLOAT8, r REAL, n NUMERIC(10, 2), i INTEGER, s VARCHAR(10));
SELECT int4(f) AS a, int4(r) AS b, int4(n) AS c, int4(i) AS d, int4(s) AS e, int4(NULL) AS h FROM measures;
WITH sales AS (SELECT 12.5 AS amount) SELECT int4(amount) AS g FROM sales;
```

##### Output Code:

##### Snowflake

Copy code

```
CREATE TABLE measures (
  f FLOAT8,
  r REAL,
  n NUMERIC(10, 2),
  i INTEGER,
  s VARCHAR(10)
)
;
SELECT
  f :: INTEGER /*** SSC-FDM-RS0029 - REDSHIFT TRUNCATES A FRACTIONAL VALUE FROM TABLE ROWS AND ROUNDS A FLOATING-POINT CONSTANT HALF TO EVEN WHEN IT CASTS THE VALUE TO AN INTEGER TYPE. SNOWFLAKE ROUNDS HALF AWAY FROM ZERO, SO VALUES MAY DIFFER. ***/ AS a,
  r :: INTEGER /*** SSC-FDM-RS0029 - REDSHIFT TRUNCATES A FRACTIONAL VALUE FROM TABLE ROWS AND ROUNDS A FLOATING-POINT CONSTANT HALF TO EVEN WHEN IT CASTS THE VALUE TO AN INTEGER TYPE. SNOWFLAKE ROUNDS HALF AWAY FROM ZERO, SO VALUES MAY DIFFER. ***/ AS b,
  n :: INTEGER /*** SSC-FDM-RS0029 - REDSHIFT TRUNCATES A FRACTIONAL VALUE FROM TABLE ROWS AND ROUNDS A FLOATING-POINT CONSTANT HALF TO EVEN WHEN IT CASTS THE VALUE TO AN INTEGER TYPE. SNOWFLAKE ROUNDS HALF AWAY FROM ZERO, SO VALUES MAY DIFFER. ***/ AS c,
  i :: INTEGER AS d,
  s :: INTEGER AS e,
  NULL :: INTEGER AS h
FROM
  measures;
WITH sales AS
(
  SELECT
    12.5 AS amount
)
SELECT
  amount :: INTEGER /*** SSC-FDM-RS0029 - REDSHIFT TRUNCATES A FRACTIONAL VALUE FROM TABLE ROWS AND ROUNDS A FLOATING-POINT CONSTANT HALF TO EVEN WHEN IT CASTS THE VALUE TO AN INTEGER TYPE. SNOWFLAKE ROUNDS HALF AWAY FROM ZERO, SO VALUES MAY DIFFER. ***/ AS g
FROM
  sales;
```

#### Best Practices

Compare the converted statement with the Redshift behavior that SSC-FDM-RS0029 describes. If that difference changes the result your workload needs, adjust the Snowflake statement before you run it.
