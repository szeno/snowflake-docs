# Object identifiers

An identifier is a string of characters (up to 255 characters in length) used to identify first-class Snowflake “named” objects, including table columns:

- Identifiers are specified at object creation time and then are referenced in queries and DDL/DML statements.
- Identifiers can also be defined in queries as aliases (e.g. `SELECT a+b AS "the sum";`).

Object identifiers, often simply referred to as object *names*, must be unique within the context of the object type and the “parent” object:

Account:
:   Identifiers for account objects (users, roles, warehouses, databases, etc.) must be unique across the entire account.

Databases:
:   Identifiers for schemas must be unique within the database. To enable resolving schemas that have the same identifiers across databases,
    Snowflake supports fully-qualifying the schema identifiers in the form of:

    `<database_name>.<schema_name>`

Schemas:
:   Identifiers for schema objects (tables, views, file formats, stages, etc.) must be unique within the schema. To enable resolving objects
    that have the same identifiers in different databases/schemas, Snowflake supports fully-qualifying the object identifiers in the form of:

    `<database_name>.<schema_name>.<object_name>`

Tables:
:   Identifiers for columns must be unique within the table.

Note

UDFs and stored procedures are schema objects; however Snowflake supports UDFs/stored procedures with the same identifier within the same schema
(also referred to as “overloading”). For more details, see [Naming and overloading procedures and UDFs](/developer-guide/udf-stored-procedure-naming-conventions).

**Next Topics:**

- [Identifier requirements](/sql-reference/identifiers-syntax)
- [Literals and variables as identifiers with IDENTIFIER() syntax](/sql-reference/identifier-literal)
- [Object name resolution](/sql-reference/name-resolution)
