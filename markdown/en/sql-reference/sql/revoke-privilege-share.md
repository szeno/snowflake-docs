# REVOKE *<privilege>* … FROM SHARE

Revokes access privileges for databases and other supported database objects (schemas, tables, and views) from a share. Revoking
privileges on these objects effectively removes the objects from the share, disabling access to the objects granted via the database
role in all consumer accounts that have created a database from the share.

For more details, see [About Secure Data Sharing](/user-guide/data-sharing-intro) and [Create and configure shares](/user-guide/data-sharing-provider).

See also:
:   [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share)

    [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege)

## Syntax

Copy code

```
REVOKE objectPrivilege ON
     {  DATABASE <name>
      | SCHEMA <name>
      | SEMANTIC VIEW <name>
      | { TABLE <name> | ALL TABLES IN SCHEMA <schema_name> }
      | { EXTERNAL TABLE <name> | ALL EXTERNAL TABLES IN SCHEMA <schema_name> }
      | { ICEBERG TABLE <name> | ALL ICEBERG TABLES IN SCHEMA <schema_name> }
      | { DYNAMIC TABLE <name> | ALL DYNAMIC TABLES IN SCHEMA <schema_name> }
      | { VIEW <name> | ALL VIEWS IN SCHEMA <schema_name> }  }
  FROM SHARE <share_name>
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
:   Specifies the identifier for the object (database, schema, table, or view) for which the specified privilege is revoked.

`schema_name`
:   Specifies the identifier for the schema for which the specified privilege is revoked for all tables or views.

`share_name`
:   Specifies the identifier for the share for which the specified privilege is revoked.

## Usage notes

- Each object privilege must be revoked individually from a share, except for tables, Apache Iceberg™ tables, and views.
  Using an `ALL` clause, you can revoke the SELECT privilege on all tables in the specified schema from a share.
  You can also revoke the SELECT privilege on all views in a schema from a share if the share has
  [SECURE\_OBJECTS\_ONLY=FALSE](/user-guide/data-sharing-views).
- If you specify a `TABLE` object that is an *Iceberg* table, the command revokes the privilege from that Iceberg table.

## Examples

> Copy code
>
> ```
> REVOKE SELECT ON VIEW mydb.shared_schema.view1 FROM SHARE share1;
>
> REVOKE SELECT ON VIEW mydb.shared_schema.view3 FROM SHARE share1;
>
> REVOKE USAGE ON SCHEMA mydb.shared_schema FROM SHARE share1;
>
> REVOKE SELECT ON ALL TABLES IN SCHEMA mydb.public FROM SHARE share1;
>
> REVOKE SELECT ON ALL ICEBERG TABLES IN SCHEMA mydb.public FROM SHARE share1;
>
> REVOKE SELECT ON ALL DYNAMIC TABLES IN SCHEMA mydb.public FROM SHARE share1;
>
> REVOKE SELECT ON ICEBERG TABLE mydb.shared_schema.iceberg_table_1 FROM SHARE share1;
>
> REVOKE SELECT ON DYNAMIC TABLE mydb TO SHARE share1;
>
> REVOKE USAGE ON SCHEMA mydb.public FROM SHARE share1;
>
> REVOKE USAGE ON DATABASE mydb FROM SHARE share1;
> ```

This example disallows a shared secure view to reference objects from a different database:

> Copy code
>
> ```
> REVOKE REFERENCE_USAGE ON DATABASE database2 FROM SHARE share1;
> ```
