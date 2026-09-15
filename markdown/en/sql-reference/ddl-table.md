# Table, view, & sequence DDL

Tables and views are the primary objects created and maintained in database schemas:

- All data in Snowflake is stored in tables.
- Views can be used to display selected rows and columns in one or more tables.

Sequences are also schema-level objects. Sequences can be used to generate unique numbers across sessions and statements or to generate
values for a primary key or any column that requires a unique value.

## Table management

- [CREATE TABLE](/sql-reference/sql/create-table)
- [CREATE TABLE … CLONE](/sql-reference/sql/create-clone)
- [CREATE TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint)
- [ALTER TABLE](/sql-reference/sql/alter-table)
- [ALTER TABLE … ALTER COLUMN](/sql-reference/sql/alter-table-column)
- [ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint)
- [DROP TABLE](/sql-reference/sql/drop-table)
- [UNDROP TABLE](/sql-reference/sql/undrop-table)
- [SHOW TABLES](/sql-reference/sql/show-tables) (also [SHOW OBJECTS](/sql-reference/sql/show-objects))
- [SHOW COLUMNS](/sql-reference/sql/show-columns)
- [DESCRIBE TABLE](/sql-reference/sql/desc-table)
- [DESCRIBE SEARCH OPTIMIZATION](/sql-reference/sql/desc-search-optimization)

## Event table management

- [CREATE EVENT TABLE](/sql-reference/sql/create-event-table)
- [ALTER TABLE (event tables)](/sql-reference/sql/alter-table-event-table)
- [DROP TABLE](/sql-reference/sql/drop-table)
- [SHOW EVENT TABLES](/sql-reference/sql/show-event-tables)
- [DESCRIBE EVENT TABLE](/sql-reference/sql/desc-event-table)

## External table management

- [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table)
- [ALTER EXTERNAL TABLE](/sql-reference/sql/alter-external-table)
- [DROP EXTERNAL TABLE](/sql-reference/sql/drop-external-table)
- [SHOW EXTERNAL TABLES](/sql-reference/sql/show-external-tables) (also [SHOW OBJECTS](/sql-reference/sql/show-objects))
- [DESCRIBE EXTERNAL TABLE](/sql-reference/sql/desc-external-table)

## Standard view management

- [CREATE VIEW](/sql-reference/sql/create-view)
- [ALTER VIEW](/sql-reference/sql/alter-view)
- [DROP VIEW](/sql-reference/sql/drop-view)
- [SHOW VIEWS](/sql-reference/sql/show-views) (also [SHOW OBJECTS](/sql-reference/sql/show-objects))
- [SHOW COLUMNS](/sql-reference/sql/show-columns)
- [DESCRIBE VIEW](/sql-reference/sql/desc-view)

## Materialized view management

- [CREATE MATERIALIZED VIEW](/sql-reference/sql/create-materialized-view)
- [ALTER MATERIALIZED VIEW](/sql-reference/sql/alter-materialized-view)
- [DROP MATERIALIZED VIEW](/sql-reference/sql/drop-materialized-view)
- [SHOW MATERIALIZED VIEWS](/sql-reference/sql/show-materialized-views)
- [DESCRIBE MATERIALIZED VIEW](/sql-reference/sql/desc-materialized-view)

## Sequence management

- [CREATE SEQUENCE](/sql-reference/sql/create-sequence)
- [CREATE SEQUENCE … CLONE](/sql-reference/sql/create-clone)
- [ALTER SEQUENCE](/sql-reference/sql/alter-sequence)
- [DROP SEQUENCE](/sql-reference/sql/drop-sequence)
- [SHOW SEQUENCES](/sql-reference/sql/show-sequences)
- [DESCRIBE SEQUENCE](/sql-reference/sql/desc-sequence)

## Column-level security management

Use these commands for Dynamic Data Masking and External Tokenization.

- [CREATE MASKING POLICY](/sql-reference/sql/create-masking-policy)
- [ALTER MASKING POLICY](/sql-reference/sql/alter-masking-policy) (see also: [ALTER TABLE](/sql-reference/sql/alter-table), [ALTER TABLE … ALTER COLUMN](/sql-reference/sql/alter-table-column), and [ALTER VIEW](/sql-reference/sql/alter-view))
- [DROP MASKING POLICY](/sql-reference/sql/drop-masking-policy)
- [SHOW MASKING POLICIES](/sql-reference/sql/show-masking-policies)
- [DESCRIBE MASKING POLICY](/sql-reference/sql/desc-masking-policy)

## Row access policy management

Snowflake supports the following DDL commands and operations to manage row access policies:

- [CREATE ROW ACCESS POLICY](/sql-reference/sql/create-row-access-policy)
- [ALTER ROW ACCESS POLICY](/sql-reference/sql/alter-row-access-policy)
- [DROP ROW ACCESS POLICY](/sql-reference/sql/drop-row-access-policy)
- [SHOW ROW ACCESS POLICIES](/sql-reference/sql/show-row-access-policies)
- [DESCRIBE ROW ACCESS POLICY](/sql-reference/sql/desc-row-access-policy)
- [ALTER TABLE](/sql-reference/sql/alter-table), [ALTER EXTERNAL TABLE](/sql-reference/sql/alter-external-table), and [ALTER VIEW](/sql-reference/sql/alter-view) (to add/drop a policy on a table or view)
