# GRANT *<privilege>* … TO SHARE

Grants access privileges for databases and other supported database objects (schemas, UDFs, tables, and views) to a share. Granting
privileges on these objects effectively adds the objects to the share, which can then be shared with one or more consumer accounts.

For more details, see [About Secure Data Sharing](/user-guide/data-sharing-intro) and [Create and configure shares](/user-guide/data-sharing-provider).

See also:
:   [REVOKE <privilege> … FROM SHARE](/sql-reference/sql/revoke-privilege-share)

    [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege)

## Syntax

Copy code

```
GRANT objectPrivilege ON
     {  DATABASE <name>
      | SCHEMA <name>
      | FUNCTION <name>
      | SEMANTIC VIEW <name>
      | { TABLE <name> | ALL TABLES IN SCHEMA <schema_name> }
      | { EXTERNAL TABLE <name> | ALL EXTERNAL TABLES IN SCHEMA <schema_name> }
      | { ICEBERG TABLE <name> | ALL ICEBERG TABLES IN SCHEMA <schema_name> }
      | { DYNAMIC TABLE <name> | ALL DYNAMIC TABLES IN SCHEMA <schema_name> }
      | TAG <name>
      | VIEW <name>  }
  TO SHARE <share_name>
```

Where:

Copy code

```
objectPrivilege ::=
-- For DATABASE
   REFERENCE_USAGE [ , ... ]
-- For DATABASE, FUNCTION, or SCHEMA
   USAGE [ , ... ]
-- For SEMANTIC VIEW
   { REFERENCES | SELECT } [ , ... ]
-- For TABLE
   EVOLVE SCHEMA [ , ... ]
-- For EXTERNAL TABLE, ICEBERG TABLE, TABLE, or VIEW
   SELECT [ , ... ]
-- For TAG
   READ
```

## Parameters

`name`
:   Specifies the identifier for the object for which the specified privilege is granted.

`schema_name`
:   Specifies the identifier for the schema for which the specified privilege is granted for all tables.

`share_name`
:   Specifies the identifier for the share from which the specified privilege is granted.

## Usage notes

- The USAGE privilege on only a single database can be granted to a share; however, within that database, privileges on multiple schemas,
  UDFs, tables, and views can be granted to the share.
- Privileges on individual objects must be granted to a share in separate GRANT statements. The only exceptions are the SELECT privilege on
  tables (including Apache Iceberg™ tables) and views. Using an `ALL` clause, you can grant SELECT on all tables in a specified schema
  to a share. You can also grant SELECT on all views in a specified schema to a share if the share has
  [SECURE\_OBJECTS\_ONLY=FALSE](/user-guide/data-sharing-views).
- By default, the SELECT privilege on views can only be granted on secure views. To share non-secure views,
  see [Share data in non-secured views](/user-guide/data-sharing-views).
- The USAGE privilege can only be granted on secure UDFs. Attempting to grant the USAGE privilege on a non-secure UDF to a share returns
  an error.
- Currently, sharing a UDF that references an object from another database is not supported. For example, if you attempt to grant USAGE
  on a UDF that references a secure view from another database, an error is returned.
- Use the REFERENCE\_USAGE privilege when sharing a secure view that references objects belonging to multiple databases, as follows:

  - The REFERENCE\_USAGE privilege must be granted individually on each database.
  - The REFERENCE\_USAGE privilege must be granted on a database before granting the SELECT privilege on a secure view to a share.

  For more details, see [Share data from multiple databases](/user-guide/data-sharing-multiple-db).
- [Secure Data Sharing](/user-guide/data-sharing-intro): Data providers cannot add new objects to a share automatically using
  future grants. That is, data providers cannot grant privileges on future objects to a share using
  GRANT *<privilege>* … TO SHARE statements.
- You cannot reshare a database or database objects created from a share. If you attempt to grant the USAGE privilege on a database or
  database objects created from a share to a different share, an error is returned.
- If you specify a `TABLE` object that is an *Iceberg* table, the command grants the privilege on that Iceberg table.

## Examples

This is an example of sharing objects from a single database:

> Copy code
>
> ```
> GRANT USAGE ON DATABASE mydb TO SHARE share1;
>
> GRANT USAGE ON SCHEMA mydb.public TO SHARE share1;
>
> GRANT USAGE ON FUNCTION mydb.shared_schema.function1 TO SHARE share1;
>
> GRANT USAGE ON FUNCTION mydb.shared_schema.function2 TO SHARE share1;
>
> GRANT SELECT ON ALL TABLES IN SCHEMA mydb.public TO SHARE share1;
>
> GRANT SELECT ON ALL EXTERNAL TABLES IN SCHEMA mydb.public TO SHARE share1;
>
> GRANT SELECT ON ALL ICEBERG TABLES IN SCHEMA mydb.public TO SHARE share1;
>
> GRANT SELECT ON ALL DYNAMIC TABLES IN SCHEMA mydb.public TO SHARE share1;
>
> GRANT USAGE ON SCHEMA mydb.shared_schema TO SHARE share1;
>
> GRANT SELECT ON VIEW mydb.shared_schema.view1 TO SHARE share1;
>
> GRANT SELECT ON VIEW mydb.shared_schema.view3 TO SHARE share1;
>
> GRANT SELECT ON ICEBERG TABLE mydb.shared_schema.iceberg_table_1 TO SHARE share1;
>
> GRANT SELECT ON DYNAMIC TABLE mydb.public TO SHARE share1;
> ```

This is an example of sharing a secure view that references objects from a different database:

> Copy code
>
> ```
> CREATE SECURE VIEW view2 AS SELECT * FROM database2.public.sampletable;
>
> GRANT USAGE ON DATABASE database1 TO SHARE share1;
>
> GRANT USAGE ON SCHEMA database1.schema1 TO SHARE share1;
>
> GRANT REFERENCE_USAGE ON DATABASE database2 TO SHARE share1;
>
> GRANT SELECT ON VIEW view2 TO SHARE share1;
> ```
