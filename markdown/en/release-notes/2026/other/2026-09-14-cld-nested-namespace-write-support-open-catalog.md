# Sep 14, 2026: Catalog-linked databases: Write support for nested namespaces

Catalog-linked databases now support creating and writing to tables in nested namespaces when the catalog-linked database uses a
catalog integration for a catalog that supports nested namespaces. Previously, creating tables and writing to tables in nested namespaces wasn’t
supported for any remote catalog.

To create a nested namespace, set the NAMESPACE\_MODE parameter to FLATTEN\_NESTED\_NAMESPACE and specify a
NAMESPACE\_FLATTEN\_DELIMITER for your catalog-linked database. Then, use CREATE SCHEMA with the flattened namespace name to create
the nested namespace. The parent namespace must already exist. Snowflake doesn’t automatically create parent namespaces.

For example, the following command creates a namespace named `namespace1a`, nested under the existing top-level namespace
`namespace1`, using a `_` delimiter:

Copy code

```
CREATE SCHEMA namespace1_namespace1a;
```

You can then create or write to Iceberg tables in the nested namespace, and use DROP SCHEMA to drop it, the same way you would for
a top-level namespace.

Caution

Don’t use a period (`.`) in a namespace name unless a period is the value you set for the NAMESPACE\_FLATTEN\_DELIMITER parameter and
NAMESPACE\_MODE is set to FLATTEN\_NESTED\_NAMESPACE. Otherwise, the namespace won’t be created.

This update also includes the following changes:

- [SHOW SCHEMAS](/sql-reference/sql/show-schemas) output now includes an `is_nested` column for all schemas. For a schema in a
  catalog-linked database, this column indicates whether the corresponding namespace is nested under another namespace in the
  remote catalog. For all other schemas, this column returns `N`.
- The NAMESPACE\_FLATTEN\_DELIMITER parameter now only supports punctuation, symbols, or digits. Letters and whitespace aren’t
  allowed.

For more information, see:

- [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database)
- [Use CREATE SCHEMA to create namespaces in your external catalog](/user-guide/tables-iceberg-externally-managed-writes#label-tables-iceberg-externally-managed-writes-create-schema)
- [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked)
