# DDL for user-defined functions, external functions, and stored procedures

UDFs (user-defined functions) and stored procedures are two programming constructs that allow you to extend Snowflake SQL.

## UDF management

UDFs can be used to perform operations that are not available via the system-defined functions provided by Snowflake. Snowflake provides the following DDL
commands for creating and managing UDFs:

- [CREATE FUNCTION](/sql-reference/sql/create-function)
- [ALTER FUNCTION](/sql-reference/sql/alter-function)
- [DROP FUNCTION](/sql-reference/sql/drop-function)
- [DESCRIBE FUNCTION](/sql-reference/sql/desc-function)
- [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions)

Note

UDFs can contain Java, JavaScript, Python, and SQL; however, DDL and DML operations are not supported in UDFs.

## External function management

External functions can be used to perform operations that are not available via the system-defined functions provided
by Snowflake. External functions are a type of UDF, but their syntax is different enough that they have their own
CREATE, ALTER, and SHOW statements.

Snowflake provides the following DDL commands for creating and managing external functions:

- [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function)
- [ALTER FUNCTION](/sql-reference/sql/alter-function)
- [DROP FUNCTION](/sql-reference/sql/drop-function)
- [SHOW EXTERNAL FUNCTIONS](/sql-reference/sql/show-external-functions)
- [DESCRIBE FUNCTION](/sql-reference/sql/desc-function)

External functions use API integrations. Snowflake provides the following DDL commands for creating and managing
API integrations:

- [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration)
- [ALTER API INTEGRATION](/sql-reference/sql/alter-api-integration)
- [DROP INTEGRATION](/sql-reference/sql/drop-integration)
- [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations)
- [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

## Stored procedure management

Snowflake provides the following DDL commands for creating and managing stored procedures:

- [CREATE PROCEDURE](/sql-reference/sql/create-procedure)
- [ALTER PROCEDURE](/sql-reference/sql/alter-procedure)
- [DROP PROCEDURE](/sql-reference/sql/drop-procedure)
- [SHOW PROCEDURES](/sql-reference/sql/show-procedures)
- [DESCRIBE PROCEDURE](/sql-reference/sql/desc-procedure)

In addition, Snowflake provides the following command for using stored procedures:

- [CALL](/sql-reference/sql/call)
