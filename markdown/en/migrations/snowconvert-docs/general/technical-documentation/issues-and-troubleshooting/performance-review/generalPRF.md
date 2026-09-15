# Code Conversion - General Performance Review Messages

## SSC-PRF-0001

This statement has usages of cursor fetch bulk operations

### Description

This warning indicates that the statement uses cursor fetch bulk operations. These operations allow you to retrieve multiple rows of data from a cursor at once, instead of one row at a time. Using bulk operations improves performance by reducing the number of communications needed between the client and server.

This pattern can become complex if not implemented correctly. For example, retrieving too many rows in a single fetch operation can consume excessive memory. It’s crucial to maintain a balance between the number of rows fetched and the available memory resources.

### Code Example

#### Oracle

##### Input

Copy code

```
 CREATE OR REPLACE PROCEDURE oracle_cursor_fetch_bulk AS
--cursor and variable declarations
BEGIN
    OPEN c1;
    FETCH c1 BULK COLLECT INTO col1;
    CLOSE c1;
END;
```

##### Output

Copy code

```
 CREATE OR REPLACE PROCEDURE oracle_cursor_fetch_bulk ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
--cursor and variable declarations
$$
    BEGIN
        OPEN c1;
        --** SSC-PRF-0001 - THIS STATEMENT HAS USAGES OF CURSOR FETCH BULK OPERATIONS **
        c1 := (
            CALL FETCH_BULK_COLLECTION_RECORDS_UDF(:c1)
        );
        col1 := :c1:RESULT;
        CLOSE c1;
    END;
$$;
```

### Best Practices

- For additional support, please contact us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-PRF-0002

Case insensitive columns can decrease performance of queries

### Description

Using collation in Snowflake can impact query performance, particularly in WHERE clauses. To learn more about how collation affects performance, please refer to the [Performance Implications of Using Collation](https://docs.snowflake.com/en/sql-reference/collation#performance-implications-of-using-collation).

A warning has been generated to indicate that a column was created with case-insensitive collation. Using this column in queries may cause slower performance.

### Code examples

#### Output

Copy code

```
 CREATE TABLE exampleTable
(
    col1 CHAR(10),
    col2 CHAR(20) COLLATE 'en-ci' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"teradata"}}'
;
```

#### Oracle

##### Input

Copy code

```
 CREATE TABLE exampleTable (
    col1 VARCHAR(50) COLLATE BINARY_CI,
    col2 VARCHAR(50) COLLATE BINARY_CS
);
```

##### Output

Copy code

```
 CREATE OR REPLACE TABLE exampleTable (
       col1 VARCHAR(50) COLLATE BINARY_CI /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/,
       col2 VARCHAR(50) COLLATE BINARY_CS
   )
   COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
   ;
```

#### Microsoft SQL Server

##### Input

Copy code

```
 CREATE TABLE exampleTable (
    col1 VARCHAR(50) COLLATE Latin1_General_CI_AS,
    col2 VARCHAR(50) COLLATE Latin1_General_CS_AS
);
```

##### Output

Copy code

```
 CREATE OR REPLACE TABLE exampleTable (
    col1 VARCHAR(50) COLLATE 'EN-CI-AS' /*** SSC-PRF-0002 - CASE INSENSITIVE COLUMNS CAN DECREASE THE PERFORMANCE OF QUERIES ***/,
    col2 VARCHAR(50) COLLATE 'EN-CS-AS'
)
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
;
```

### Best Practices

- If your application’s performance is significantly affected by case-insensitive collation, consider rewriting your code to avoid using it. However, if the performance impact is acceptable, you can ignore this warning.
- For additional assistance, contact us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-PRF-0003

Fetch inside a loop is considered a complex pattern, this could degrade Snowflake performance

### Severity

Low

### Description

This warning appears when a `FETCH` statement is detected within a loop. The `FETCH` statement retrieves and processes individual rows from a result set one at a time.

Processing large datasets using cursors within loops can become complex, especially when:

- Multiple table joins are involved
- Complex calculations are required
- Large numbers of rows need to be processed

This pattern may lead to performance issues and can be difficult to maintain as the data volume grows.

#### Code Example

#### Teradata

##### Input

Copy code

```
 REPLACE PROCEDURE teradata_fetch_inside_loop()
DYNAMIC RESULT SETS 1
BEGIN
    DECLARE col_name VARCHAR(200);
    DECLARE col_int INTEGER DEFAULT 0;
    DECLARE cursor_var CURSOR FOR SELECT some_column FROM tabla1;
    WHILE (col_int <> 0) DO
        FETCH cursor_var INTO col_name;
        SET col_int = col_int + 1;
    END WHILE;
END;
```

##### Output

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "tabla1" **
CREATE OR REPLACE PROCEDURE teradata_fetch_inside_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        col_name VARCHAR(200);
        col_int INTEGER DEFAULT 0;
    BEGIN

        LET cursor_var CURSOR
        FOR
            SELECT
                some_column FROM
                tabla1;
                WHILE (:col_int <> 0) LOOP
            --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
                    FETCH cursor_var INTO col_name;
            col_int := col_int + 1;
                END LOOP;
    END;
$$;
```

#### Oracle

##### Input

Copy code

```
 CREATE PROCEDURE oracle_fetch_inside_loop
IS
  var1 table1.column1%TYPE;
  CURSOR cursor1 IS SELECT COLUMN_NAME FROM table1;
BEGIN
  WHILE true LOOP
    FETCH cursor1 INTO var1;
    EXIT WHEN cursor1%NOTFOUND;
  END LOOP;
END;
```

##### Output

Copy code

```
 CREATE OR REPLACE PROCEDURE oracle_fetch_inside_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    var1 VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'table1.column1%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!;
    --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
    cursor1 CURSOR
    FOR
      SELECT COLUMN_NAME FROM
        table1;
  BEGIN
    WHILE (true)
                 --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                 LOOP
      --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
         FETCH cursor1 INTO
        :var1;
         IF (var1 IS NULL) THEN
        EXIT;
         END IF;
       END LOOP;
  END;
$$;
```

#### SQL Server

##### Input

Copy code

```
 CREATE OR ALTER PROCEDURE transact_fetch_inside_loop
AS
BEGIN
    DECLARE cursor1 CURSOR
        FOR SELECT col1 FROM my_table;
    WHILE 1=0
    BEGIN
       FETCH NEXT FROM @cursor1 INTO @variable1;
    END
END;
```

##### Output

Copy code

```
 CREATE OR REPLACE PROCEDURE transact_fetch_inside_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        --** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
        cursor1 CURSOR
        FOR
            SELECT
                col1
            FROM
                my_table;
    BEGIN

        WHILE (1=0) LOOP
            --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
            FETCH
                CURSOR1
                INTO
                :VARIABLE1;
        END LOOP;
    END;
$$;
```

### Best Practices

- To improve performance and avoid complex patterns, use set-based operations instead of loops. Replace row-by-row processing with SQL statements (SELECT, UPDATE, DELETE) that operate on multiple rows simultaneously using WHERE clauses. This approach is more efficient and easier to maintain.

#### Oracle

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_fetch_inside_loop
AS
  record_employee employees%rowtype;
  CURSOR emp_cursor IS SELECT * FROM employees;
BEGIN
  OPEN emp_cursor;
  LOOP
    FETCH emp_cursor INTO record_employee;
    EXIT WHEN emp_cursor%notfound;
    INSERT INTO new_employees VALUES (record_employee.first_name, record_employee.last_name);
  END LOOP;
  CLOSE emp_cursor;
END;
```

#### Snowflake

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_fetch_inside_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    record_employee OBJECT !!!RESOLVE EWI!!! /*** SSC-EWI-0036 - ROWTYPE DATA TYPE CONVERTED TO OBJECT ***/!!! := OBJECT_CONSTRUCT();
    --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
    emp_cursor CURSOR
    FOR
      SELECT
        OBJECT_CONSTRUCT( *) sc_cursor_record FROM
        employees;
  BEGIN
    OPEN emp_cursor;
    --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    LOOP
      --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
      FETCH emp_cursor INTO
        :record_employee;
      IF (record_employee IS NULL) THEN
        EXIT;
      END IF;
      INSERT INTO new_employees
      SELECT
        :record_employee:FIRST_NAME,
        :record_employee:LAST_NAME;
    END LOOP;
  CLOSE emp_cursor;
  END;
$$;
```

Set-based operations can be used to process data more efficiently.

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_fetch_inside_loop AS
BEGIN
  INSERT INTO new_employees (first_name, last_name)
  SELECT first_name, last_name FROM employees;
END;
```

Set-based operations can be used to process data more efficiently.

Copy code

```
 CREATE OR REPLACE PROCEDURE cursor_fetch_inside_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  BEGIN
    INSERT INTO new_employees(first_name, last_name)
    SELECT first_name, last_name FROM
      employees;
  END;
$$;
```

### Best Practices

- For additional support, please contact us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-PRF-0004

This statement has usages of cursor for loop

### Severity

None

### Description

This warning indicates that the statement contains cursor for loops. A cursor for loop is a programming structure that processes query results one row at a time, allowing you to work with individual records from a result set.

This warning helps identify potential performance issues in cursor FOR loops. Performance problems may arise when:

- The SELECT statement within the cursor returns a large dataset
- The loop contains complex operations
- The loop contains nested loops

While these patterns can be detected, you should review and optimize the code to ensure efficient execution.

#### Code Example

#### Teradata

##### Input

Copy code

```
 REPLACE PROCEDURE teradata_cursor_for_loop()
BEGIN
    FOR fUsgClass AS cUsgClass CURSOR FOR
        (SELECT col1
        FROM sample_table)
    DO
        SET var1 = fUsgClass.col1;
    END FOR;
END;
```

##### Output

Copy code

```
 --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "sample_table" **
CREATE OR REPLACE PROCEDURE teradata_cursor_for_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/16/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        !!!RESOLVE EWI!!! /*** SSC-EWI-0110 - TRANSFORMATION NOT PERFORMED DUE TO MISSING DEPENDENCIES ***/!!!
        temp_fUsgClass_col1;
    BEGIN
        LET cUsgClass CURSOR
        FOR
            SELECT
                col1
                   FROM
                sample_table;
        --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
        FOR fUsgClass IN cUsgClass DO
            temp_fUsgClass_col1 := fUsgClass.col1;
            var1 := :temp_fUsgClass_col1;
        END FOR;
    END;
$$;
```

#### Oracle

##### Input

Copy code

```
 CREATE OR REPLACE PROCEDURE oracle_cursor_for_loop AS
BEGIN
    FOR r1 IN (SELECT col1 FROM sample_table) LOOP
        NULL;
    END LOOP;
END;
```

##### Output

Copy code

```
 CREATE OR REPLACE PROCEDURE oracle_cursor_for_loop ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
    BEGIN
        LET temporary_for_cursor_0 CURSOR
        FOR
            (SELECT col1 FROM
                    sample_table
            );
        --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
        FOR r1 IN temporary_for_cursor_0 DO
            NULL;
        END FOR;
    END;
$$;
```

### Best Practices

- For additional support, please contact us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-PRF-0005

The statement below has usages of nested cursors

Note

For better readability, we have simplified some sections of the code in this example.

### Severity

None

### Description

This warning indicates that the statement contains nested cursors. A cursor is a database feature that lets you process rows from a query result one at a time. Nested cursors occur when you use one cursor inside another cursor’s loop, which can impact performance and should be used with caution.

Nested cursors can significantly slow down your code’s performance, particularly when working with large amounts of data. This is because each time a cursor operates, it needs to communicate with the database server, creating additional processing overhead and delays.

### Code examples

#### SQL Server

##### Input

Copy code

```
 CREATE OR ALTER PROCEDURE procedureSample
AS
BEGIN
  DECLARE
    @outer_category_id INT,
    @outer_category_name NVARCHAR(50),
    @inner_product_name NVARCHAR(50);

  -- Define the outer cursor
  DECLARE outer_cursor CURSOR FOR
    SELECT category_id, category_name FROM categories;

  -- Open the outer cursor
  OPEN @outer_cursor;

  -- Fetch the first row from the outer cursor
  FETCH NEXT FROM outer_cursor INTO @outer_category_id, @outer_category_name;

  -- Start the outer loop
  WHILE @@FETCH_STATUS = 0
  BEGIN

    PRINT 'Category: ' + @outer_category_name;

    -- Define the inner cursor
    DECLARE inner_cursor CURSOR FOR
      SELECT product_name FROM products WHERE category_id = @outer_category_id;

    -- Open the inner cursor
    OPEN inner_cursor;
	FETCH NEXT FROM inner_cursor INTO @inner_product_name;

    WHILE @@FETCH_STATUS = 0
    BEGIN
      PRINT 'Product: ' + @inner_product_name + ' Category: ' + CAST(@outer_category_id AS NVARCHAR(10));

      -- Fetch the next row from the inner cursor
      FETCH NEXT FROM inner_cursor INTO @inner_product_name;
    END;

    -- Close the inner cursor
    CLOSE inner_cursor;
    DEALLOCATE inner_cursor;

    -- Fetch the next row from the outer cursor
    FETCH NEXT FROM outer_cursor INTO @outer_category_id, @outer_category_name;
  END;

  -- Close the outer cursor
  CLOSE outer_cursor;
  DEALLOCATE outer_cursor;

END;
```

##### Output

Copy code

```
 CREATE OR REPLACE PROCEDURE procedureSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"transact"}}'
EXECUTE AS CALLER
AS
$$
	DECLARE
		OUTER_CATEGORY_ID INT;
		OUTER_CATEGORY_NAME VARCHAR(50);
		INNER_PRODUCT_NAME VARCHAR(50);

		-- Define the outer cursor
		--** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
		outer_cursor CURSOR
		FOR
			SELECT
				category_id,
				category_name
			FROM
				categories;

		-- Define the inner cursor
		--** SSC-FDM-TS0013 - SNOWFLAKE SCRIPTING CURSOR ROWS ARE NOT MODIFIABLE **
		inner_cursor CURSOR
		FOR
			SELECT
				product_name
			FROM
				products
			WHERE
				category_id = :OUTER_CATEGORY_ID;
	BEGIN

		-- Open the outer cursor
		--** SSC-PRF-0005 - THE STATEMENT BELOW HAS USAGES OF NESTED CURSORS. **
		OPEN OUTER_CURSOR;
  -- Fetch the first row from the outer cursor
		FETCH
			outer_cursor
			INTO
			:OUTER_CATEGORY_ID,
			:OUTER_CATEGORY_NAME;

			-- Start the outer loop

			  -- Define the inner cursor
			WHILE (:FETCH_STATUS = 0) LOOP
			!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'PRINT' NODE ***/!!!

			  PRINT 'Category: ' + @outer_category_name;

			-- Open the inner cursor
			OPEN inner_cursor;
			--** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
			FETCH
				inner_cursor
			INTO
				:INNER_PRODUCT_NAME;
			WHILE (:FETCH_STATUS = 0) LOOP
				!!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'PRINT' NODE ***/!!!
				PRINT 'Product: ' + @inner_product_name + ' Category: ' + CAST(@outer_category_id AS NVARCHAR(10));
				-- Fetch the next row from the inner cursor
				--** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
				FETCH
					inner_cursor
				INTO
					:INNER_PRODUCT_NAME;
			END LOOP;
			-- Close the inner cursor
			CLOSE inner_cursor;
			!!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'DEALLOCATE' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
			  DEALLOCATE inner_cursor;
			-- Fetch the next row from the outer cursor
			--** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
			FETCH
				outer_cursor
			INTO
				:OUTER_CATEGORY_ID,
				:OUTER_CATEGORY_NAME;
			END LOOP;
  -- Close the outer cursor
			CLOSE outer_cursor;
			!!!RESOLVE EWI!!! /*** SSC-EWI-0058 - FUNCTIONALITY FOR 'DEALLOCATE' IS NOT CURRENTLY SUPPORTED BY SNOWFLAKE SCRIPTING ***/!!!
			DEALLOCATE outer_cursor;
	END;
$$;
```

#### Oracle

#### Explicit cursor

##### Input

Copy code

```
 CREATE OR REPLACE PROCEDURE procedureSample AS
BEGIN
DECLARE
  CURSOR outer_cursor IS
    SELECT category_id, category_name FROM categories;

  CURSOR inner_cursor (p_category_id NUMBER) IS
    SELECT product_name FROM products WHERE category_id = p_category_id;

  outer_category_id categories.category_id%TYPE;
  outer_category_name categories.category_name%TYPE;
  inner_product_name products.product_name%TYPE;
BEGIN

  OPEN outer_cursor;
  FETCH outer_cursor INTO outer_category_id, outer_category_name;

  LOOP
    EXIT WHEN outer_cursor%NOTFOUND;
    DBMS_OUTPUT.PUT_LINE('Category: ' || outer_category_name);

    OPEN inner_cursor(outer_category_id);
    LOOP
        FETCH inner_cursor INTO inner_product_name;
        EXIT WHEN inner_cursor%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE('Product: ' || inner_product_name || ' Category: ' || outer_category_id);
    END LOOP;
    CLOSE inner_cursor;

    FETCH outer_cursor INTO outer_category_id, outer_category_name;
  END LOOP;

  CLOSE outer_cursor;
END;
END;
```

##### Output

Copy code

```
 CREATE OR REPLACE PROCEDURE procedureSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
  BEGIN
    DECLARE
      --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
      outer_cursor CURSOR
      FOR
        SELECT category_id, category_name FROM
          categories;
      --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
      inner_cursor CURSOR
      FOR
        SELECT product_name FROM
          products
        WHERE category_id = ?;
      outer_category_id VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'categories.category_id%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!;
      outer_category_name VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'categories.category_name%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!;
      inner_product_name VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'products.PRODUCT_NAME%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!;
      call_results VARIANT;
    BEGIN
      --** SSC-PRF-0005 - THE STATEMENT BELOW HAS USAGES OF NESTED CURSORS. **
      OPEN outer_cursor USING ('DEFAULT VALUE NOT FOUND');
      FETCH outer_cursor INTO
        :outer_category_id,
        :outer_category_name;
      --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
      LOOP
        IF (outer_category_id IS NULL) THEN
          EXIT;
        END IF;
        --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
        call_results := (
          CALL DBMS_OUTPUT.PUT_LINE_UDF('Category: ' || NVL(:outer_category_name :: STRING, ''))
        );
        OPEN inner_cursor USING (:outer_category_id);
        --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
        LOOP
          --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
            FETCH inner_cursor INTO
            :inner_product_name;
          IF (inner_product_name IS NULL) THEN
            EXIT;
          END IF;
          --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
          call_results := (
            CALL DBMS_OUTPUT.PUT_LINE_UDF('Product: ' || NVL(:inner_product_name :: STRING, '') || ' Category: ' || NVL(:outer_category_id :: STRING, ''))
          );
        END LOOP;
        CLOSE inner_cursor;
        --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
        FETCH outer_cursor INTO
          :outer_category_id,
          :outer_category_name;
      END LOOP;
      CLOSE outer_cursor;
      RETURN call_results;
    END;
  END;
$$;
```

#### Implicit Cursor

##### Input

Copy code

```
 CREATE OR REPLACE PROCEDURE procedureSample AS
BEGIN
DECLARE
   inner_category_id categories.category_name%TYPE;
   inner_product_name products.product_name%TYPE;
   inner_cursor SYS_REFCURSOR;
BEGIN
   FOR outer_cursor IN (SELECT category_id, category_name FROM categories)
   LOOP
      OPEN inner_cursor
       FOR SELECT product_name, category_id FROM products WHERE category_id = outer_cursor.category_id;
      LOOP
         FETCH inner_cursor INTO inner_product_name, inner_category_id;
         EXIT WHEN inner_cursor%NOTFOUND;
         dbms_output.put_line( 'Category id: '|| outer_cursor.category_id);
         dbms_output.put_line('Product name: ' || inner_product_name);
      END LOOP;
      CLOSE inner_cursor;
   END LOOP;
END;
END;
```

##### Output

Copy code

```
 CREATE OR REPLACE PROCEDURE procedureSample ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "oracle",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
EXECUTE AS CALLER
AS
$$
   BEGIN
      DECLARE
         inner_category_id VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'categories.category_name%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!;
         inner_product_name VARIANT !!!RESOLVE EWI!!! /*** SSC-EWI-OR0129 - TYPE ATTRIBUTE 'products.product_name%TYPE' COULD NOT BE RESOLVED, SO IT WAS TRANSFORMED TO VARIANT ***/!!!;
         inner_cursor_res RESULTSET;
         call_results VARIANT;
      BEGIN
         LET temporary_for_cursor_0 CURSOR
         FOR
            (SELECT category_id, category_name FROM
                  categories
            );
         --** SSC-PRF-0004 - THIS STATEMENT HAS USAGES OF CURSOR FOR LOOP **
         --** SSC-PRF-0005 - THE STATEMENT BELOW HAS USAGES OF NESTED CURSORS. **
         FOR outer_cursor IN temporary_for_cursor_0 DO
            LET inner_cursor CURSOR
            FOR
               SELECT product_name, category_id FROM
                  products
               WHERE category_id = outer_cursor.category_id;
            OPEN inner_cursor;
            --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
                 LOOP
               --** SSC-PRF-0003 - FETCH INSIDE A LOOP IS CONSIDERED A COMPLEX PATTERN, THIS COULD DEGRADE SNOWFLAKE PERFORMANCE. **
                    FETCH inner_cursor INTO
                  :inner_product_name,
                  :inner_category_id;
               IF (inner_product_name IS NULL) THEN
                  EXIT;
               END IF;
               --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
               call_results := (
                  CALL dbms_output.put_line( 'Category id: ' || NVL(outer_cursor.category_id :: STRING, ''))
               );
               --** SSC-FDM-OR0035 - CHECK UDF IMPLEMENTATION FOR DBMS_OUTPUT.PUT_LINE_UDF. **
               call_results := (
                  CALL dbms_output.put_line('Product name: ' || NVL(:inner_product_name :: STRING, ''))
               );
                 END LOOP;
                 CLOSE inner_cursor;
         END FOR;
         RETURN call_results;
      END;
   END;
$$;
```

### Best Practices

- Nested cursors should be avoided as they can negatively impact performance and make code more complex.
- Instead of nested cursors, use SQL features such as:
  - SQL functions
  - Joins
  - Subqueries
  - Window functions
  - Common Table Expressions (CTEs)
  - Recursive queries
    These alternatives process data in bulk and are more efficient.
- For additional assistance, contact us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-PRF-0006

Nested cursor inside query is not supported in Snowflake

### Severity

None

### Description

This message appears when a query contains a cursor definition. When a cursor expression is evaluated, it returns and automatically opens a nested cursor. For more details, see [Oracle Cursor Expression](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CURSOR-Expressions.html#GUID-B28362BE-8831-4687-89CF-9F77DB3698D2).

### Code examples

#### Input

Copy code

```
 SELECT
  category_id,
  category_name,
  CURSOR (
    SELECT
      product_id,
      product_name || ', ' || category_id
    FROM
      products e
    WHERE
      e.category_id = d.category_id
  ) EMP_CUR
FROM
  categories d;
```

#### Output

Copy code

```
 SELECT
  category_id,
  category_name,
  --** SSC-PRF-0006 - NESTED CURSOR INSIDE QUERY IS NOT SUPPORTED IN SNOWFLAKE. **
  CURSOR
    !!!RESOLVE EWI!!! /*** SSC-EWI-0108 - THE FOLLOWING SUBQUERY MATCHES AT LEAST ONE OF THE PATTERNS CONSIDERED INVALID AND MAY PRODUCE COMPILATION ERRORS ***/!!! (
    SELECT
      product_id,
      NVL(
      product_name :: STRING, '') || ', ' || NVL(category_id :: STRING, '')
    FROM
      products e
    WHERE
      e.category_id = d.category_id
  ) EMP_CUR
FROM
  categories d;
```

### Best Practices

- We recommend avoiding cursors as they can negatively affect performance and make code more complex.
- Instead of using nested cursors, consider these alternatives:
  - SQL functions
  - Joins
  - Subqueries
  - Window functions
  - Common Table Expressions (CTEs)
  - Recursive queries
    These options are better for processing large amounts of data efficiently.
- For additional assistance, contact us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-PRF-0007

PERFORMANCE REVIEW - CLUSTER BY

### Description

Marks where the usage of CLUSTER BY may cause performance issues.

#### Example Code

##### Teradata:

Copy code

```
 CREATE MULTISET TABLE T_2008,
NO FALLBACK,
NO BEFORE JOURNAL,
NO AFTER JOURNAL,
CHECKSUM = DEFAULT,
DEFAULT MERGEBLOCKRATIO
(
      COL1 NUMBER(20,0) NOT NULL,
      COL2 INTEGER,
      COL3 VARCHAR(4) CHARACTER SET LATIN NOT CASESPECIFIC,
      COL4 DATE FORMAT 'YYYY-MM-DD'
)
PRIMARY INDEX
(
      COL1, COL2
)
PARTITION BY ( RANGE_N(COL4 BETWEEN DATE '2010-01-01' AND DATE '2025-12-31' EACH INTERVAL '1' YEAR ),
CASE_N(
COL3  = 'T',
COL3 = 'M',
COL3 = 'L') ); -- PARTITION BY transformed to CLUSTER BY
```

##### Snowflake:

Copy code

```
CREATE OR REPLACE TABLE T_2008
(
      COL1 NUMBER(20,0) NOT NULL,
      COL2 INTEGER,
      COL3 VARCHAR(4),
      COL4 DATE
)
--** SSC-PRF-0007 - PERFORMANCE REVIEW - CLUSTER BY **
CLUSTER BY (
             !!!RESOLVE EWI!!! /*** SSC-EWI-0031 - RANGE_N FUNCTION NOT SUPPORTED ***/!!!
             RANGE_N(COL4 BETWEEN DATE '2010-01-01' AND DATE '2025-12-31' EACH INTERVAL '1' YEAR ),
!!!RESOLVE EWI!!! /*** SSC-EWI-0031 - CASE_N FUNCTION NOT SUPPORTED ***/!!!
CASE_N(
COL3  = 'T',
COL3 = 'M',
COL3 = 'L'))
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "teradata",  "convertedOn": "07/02/2025",  "domain": "no-domain-provided" }}'
; -- PARTITION BY transformed to CLUSTER BY
```

##### Transact:

Copy code

```
 CREATE TABLE my_table (
    enterprise_cif INT,
    name NVARCHAR(100),
    address NVARCHAR(255),
    created_at DATETIME
)
WITH (
    DISTRIBUTION = HASH(enterprise_cif),
    CLUSTERED INDEX (enterprise_cif)
);
```

##### Snowflake:

Copy code

```
 CREATE OR REPLACE TABLE my_table (
  enterprise_cif INT,
  name VARCHAR(100),
  address VARCHAR(255),
  created_at TIMESTAMP_NTZ(3)
)
--** SSC-PRF-0007 - PERFORMANCE REVIEW - CLUSTER BY **
CLUSTER BY (enterprise_cif)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "10/09/2024" }}'
;
```

#### Best Practices

- Review the code in order to identify possible performance issues. More information about this topic can be read [here](https://docs.snowflake.com/en/user-guide/tables-clustering-keys.html).
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-PRF-0008

### Description

This message appears when loop usage is detected in procedural code. Loops such as `LOOP`, `WHILE`, and `FOR` can lead to row-by-row processing and may degrade performance in Snowflake, especially when the loop iterates over large datasets or contains complex logic. The message is informational and prompts a review of the pattern.

#### Code Example

##### PostgreSQL:

Copy code

```
CREATE OR REPLACE FUNCTION loop_example() RETURNS void AS $$
BEGIN
  FOR i IN 1..10 LOOP
    NULL;
  END LOOP;
END;
$$ LANGUAGE plpgsql;
```

##### Snowflake:

Copy code

```
CREATE OR REPLACE PROCEDURE loop_example ()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
  BEGIN
    --** SSC-PRF-0008 - PERFORMANCE REVIEW - LOOP USAGE **
    FOR i IN 1 TO 10
                     LOOP
      NULL;
    END LOOP;
  END;
$$;
;
```

### Best practices

- Prefer set-based SQL operations (SELECT, INSERT, UPDATE, DELETE) over row-by-row loops.
- Avoid nested loops when possible; use joins, CTEs, or window functions instead.
- If loops are required, keep iterations small and limit expensive operations inside the loop.
- Consider refactoring procedural logic into single statements or bulk operations.

## SSC-PRF-0009

CURSOR usage review

### Severity

None

### Description

This message appears when a cursor declaration is detected in procedural code. Cursors allow row-by-row processing of query results, which can lead to performance issues in Snowflake, especially when processing large datasets.

While cursors are valid in Snowflake Scripting, they introduce overhead because:

- Each row is processed individually rather than as a set
- Multiple round trips to the database may be required
- Memory usage can be higher compared to set-based operations

This warning is informational and prompts a review of whether the cursor usage is necessary or can be replaced with more efficient set-based operations.

### Code Example

#### Oracle

##### Input

Copy code

```
CREATE OR REPLACE PROCEDURE get_first_employee AS
  CURSOR emp_cursor IS SELECT employee_id, first_name FROM employees;
  v_emp_id NUMBER;
  v_name VARCHAR2(100);
BEGIN
  OPEN emp_cursor;
  FETCH emp_cursor INTO v_emp_id, v_name;
  CLOSE emp_cursor;
END;
```

##### Output

Copy code

```
CREATE OR REPLACE PROCEDURE get_first_employee ()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
EXECUTE AS CALLER
AS
$$
  DECLARE
    --** SSC-PRF-0009 - PERFORMANCE REVIEW - CURSOR USAGE **
    emp_cursor CURSOR
    FOR
      SELECT employee_id, first_name FROM
        employees;
    v_emp_id NUMBER(38, 18);
    v_name VARCHAR(100);
  BEGIN
    OPEN emp_cursor;
    FETCH emp_cursor INTO
      :v_emp_id,
      :v_name;
    CLOSE emp_cursor;
  END;
$$;
```

### Best Practices

- Replace cursor-based row-by-row processing with set-based SQL operations (SELECT, INSERT, UPDATE, DELETE) whenever possible.
- Use JOINs, subqueries, CTEs (Common Table Expressions), or window functions instead of cursors to process multiple rows efficiently.
- If cursors are unavoidable, minimize the work done inside the cursor loop and avoid nested cursors.
- Consider using MERGE statements for upsert operations instead of cursor-based conditional INSERT/UPDATE logic.
- For additional assistance, contact us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-PRF-0010

Partition by removed, at least one of the specified expressions have no iceberg partition transform equivalent

### Severity

None

### Description

Snowflake supports the PARTITION BY clause in Iceberg tables, however, only [Iceberg partition transforms](https://iceberg.apache.org/spec/#partition-transforms) are supported. When transforming partitioning into Iceberg tables, equivalent partition transforms are generated for supported cases. When no partition transform equivalent can be generated for the partition expressions, the PARTITION BY will be removed from the table by commenting it out with this PRF.

This PRF is only generated when tables are migrated into Iceberg tables using the tables translation conversion setting in the SnowConvert AI Desktop application.

### Code examples

#### Input

Copy code

```
 -- Additional Params: --TablesTransformationTarget SnowflakeIceberg
CREATE TABLE FINANCE.FINANCE_TABLE
(
  customerName VARCHAR(30),
  accountBalance VARCHAR(20)
)
PARTITION BY CASE_N(
accountBalance <  0 ,
accountBalance >=  0);
```

#### Output

Copy code

```
 -- Additional Params: --TablesTransformationTarget SnowflakeIceberg
CREATE OR REPLACE ICEBERG TABLE FINANCE.FINANCE_TABLE
  (
 customerName VARCHAR,
 accountBalance VARCHAR
  )
  CATALOG = 'SNOWFLAKE'
--  --** SSC-PRF-0010 - PARTITION BY REMOVED, AT LEAST ONE OF THE SPECIFIED EXPRESSIONS HAVE NO ICEBERG PARTITION TRANSFORM EQUIVALENT **
--  PARTITION BY CASE_N(
--  accountBalance <  0 ,
--  accountBalance >=  0)
  COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 1,  "minor": 0,  "patch": "0.0" }, "attributes": {  "component": "teradata",  "convertedOn": "12/16/2025",  "domain": "no-domain-provided",  "migrationid": "9CebAVkM33qsfTnTrMh3Dw==" }}'
;
```

### Best Practices

- Analyze the impact of partitioning in the performance of queries over the generated Iceberg tables, if the difference is negligible then this PRF can be safely ignored.
- For additional assistance, contact us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)
