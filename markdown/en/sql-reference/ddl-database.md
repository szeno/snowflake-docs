# Database, schema, & share DDL

Databases and schemas are used to organize data stored in Snowflake:

- A database is a logical grouping of schemas. Each database belongs to a single Snowflake account.
- A schema is a logical grouping of database objects (tables, views, etc.). Each schema belongs to a single database.

Together, a database and schema comprise a *namespace* in Snowflake. When performing any operations on database objects in Snowflake, the
namespace is inferred from the current database and schema in use for the session. If a database and schema are not in use for the session,
the namespace must be explicitly specified when performing any operations on the objects.

Snowflake provides a full set of DDL commands for creating and managing databases and schemas.

In addition, Snowflake provides DDL for creating and managing shares. A share specifies a set of database objects (schemas, tables, and
secure views) containing data you wish to share with other Snowflake accounts.

## Database management

- [CREATE DATABASE](/sql-reference/sql/create-database)
- [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked)
- [CREATE DATABASE … CLONE](/sql-reference/sql/create-clone)
- [ALTER DATABASE](/sql-reference/sql/alter-database)
- [ALTER DATABASE (catalog-linked)](/sql-reference/sql/alter-database-catalog-linked)
- [DESCRIBE DATABASE](/sql-reference/sql/desc-database)
- [DROP DATABASE](/sql-reference/sql/drop-database)
- [UNDROP DATABASE](/sql-reference/sql/undrop-database)
- [USE DATABASE](/sql-reference/sql/use-database)
- [SHOW DATABASES](/sql-reference/sql/show-databases)

## Schema management

- [CREATE SCHEMA](/sql-reference/sql/create-schema)
- [CREATE SCHEMA … CLONE](/sql-reference/sql/create-clone)
- [ALTER SCHEMA](/sql-reference/sql/alter-schema)
- [DROP SCHEMA](/sql-reference/sql/drop-schema)
- [UNDROP SCHEMA](/sql-reference/sql/undrop-schema)
- [USE SCHEMA](/sql-reference/sql/use-schema)
- [SHOW SCHEMAS](/sql-reference/sql/show-schemas)

## Share management

- [CREATE SHARE](/sql-reference/sql/create-share)
- [ALTER SHARE](/sql-reference/sql/alter-share)
- [DROP SHARE](/sql-reference/sql/drop-share)
- [SHOW SHARES](/sql-reference/sql/show-shares)
- [DESCRIBE SHARE](/sql-reference/sql/desc-share)
