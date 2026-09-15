# Data Definition Language (DDL) commands

DDL commands are used to create, manipulate, and modify objects in Snowflake, such as users, virtual warehouses, databases, schemas,
tables, views, columns, functions, and stored procedures.

They are also used to perform many account-level and session operations, such as setting parameters, initializing variables, and
initiating transactions.

The following commands serve as the base for all DDL commands:

- [ALTER <object>](/sql-reference/sql/alter)
- [COMMENT](/sql-reference/sql/comment)
- [CREATE <object>](/sql-reference/sql/create)
- [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter)
- [DESCRIBE <object>](/sql-reference/sql/desc)
- [DROP <object>](/sql-reference/sql/drop)
- [SHOW <objects>](/sql-reference/sql/show)
- [USE <object>](/sql-reference/sql/use)

Each command takes an *object type* and *identifier*, as well as additional parameters and options. The descriptions for the
[individual commands](/sql-reference/sql-all) provide the syntax and full list of parameters that can be specified for each
command. The descriptions also provide detailed usage notes and examples.

The commands are grouped into the following categories:

- [Account & session DDL](/sql-reference/ddl-other)
- [User & security DDL](/sql-reference/ddl-user-security)
- [Warehouse & resource monitor DDL](/sql-reference/ddl-virtual-warehouse)
- [Database, schema, & share DDL](/sql-reference/ddl-database)
- [Table, view, & sequence DDL](/sql-reference/ddl-table)
- [Data loading / unloading DDL](/sql-reference/ddl-stage)
- [DDL for user-defined functions, external functions, and stored procedures](/sql-reference/ddl-udf)
- [Data pipeline DDL](/sql-reference/ddl-pipeline)
- [Listings DDL](/sql-reference/ddl-listings)
- [Machine learning model DDL](/sql-reference/ddl-model)
