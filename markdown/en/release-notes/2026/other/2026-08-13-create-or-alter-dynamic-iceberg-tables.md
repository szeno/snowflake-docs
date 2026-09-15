# Aug 13, 2026: CREATE OR ALTER support for dynamic Apache Iceberg™ tables

You can now use `CREATE OR ALTER DYNAMIC ICEBERG TABLE` to create a dynamic Apache Iceberg™ table if it doesn’t exist or
alter an existing one in place. The statement represents the complete target state: properties you don’t specify
reset to their default values, and the command doesn’t trigger a refresh by itself.

For an existing dynamic Iceberg table, changing `EXTERNAL_VOLUME`, `CATALOG`, or `BASE_LOCATION` isn’t supported. You
also can’t convert a regular dynamic table into a dynamic Iceberg table or convert a dynamic Iceberg table into a
regular dynamic table.

For more information, see [CREATE OR ALTER DYNAMIC ICEBERG TABLE](/sql-reference/sql/create-dynamic-table#label-create-or-alter-dit-syntax).
