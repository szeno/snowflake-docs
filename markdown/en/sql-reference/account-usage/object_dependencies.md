Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# OBJECT\_DEPENDENCIES view

This Account Usage view displays object dependencies. An object dependency results when an object references a base object but does not
materialize or copy data, such as when a view references a table.

For example, while creating a view from a single table, the view is dependent on the table. Snowflake returns one row to record the
dependency of the view on the table.

However, if creating the view is dependent on two tables, Snowflake returns one row to record the dependency of the view on the first table
and, separately, one row to record the dependency of the view on the second table. This pattern continues for however many dependencies
there are for a given object.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| REFERENCED\_DATABASE | TEXT | The parent database of the referenced object. |
| REFERENCED\_SCHEMA | TEXT | The parent schema of the referenced object. |
| REFERENCED\_OBJECT\_NAME | TEXT | The name of the referenced object. |
| REFERENCED\_OBJECT\_ID | NUMBER | The object ID of the referenced object. |
| REFERENCED\_OBJECT\_DOMAIN | TEXT | The domain (e.g. `TABLE`, `VIEW`) of the referenced object. |
| REFERENCING\_DATABASE | TEXT | The parent database of the referencing object. |
| REFERENCING\_SCHEMA | TEXT | The parent schema of the referencing object. |
| REFERENCING\_OBJECT\_NAME | TEXT | The name of the referencing object. |
| REFERENCING\_OBJECT\_ID | NUMBER | The object ID of the referencing object. |
| REFERENCING\_OBJECT\_DOMAIN | TEXT | The domain (e.g. `TABLE`, `VIEW`) of the referencing object. |
| DEPENDENCY\_TYPE | TEXT | The type of dependency (`BY_ID`, `BY_NAME`, or `BY_NAME_AND_ID`). |

Expand

Show lessSee more

## Usage notes

- Latency for this view may be up to three hours.

- For a complete list of supported objects and their dependency type, see [Supported object dependencies](/user-guide/object-dependencies#label-object-dependencies-supported-objects).
- Data movement, such as when data is copied or materialized from one object to another, does not result in an object dependency. For
  example, CREATE TABLE AS SELECT (CTAS), INSERT, or MERGE operations on tables result in data movement and are not included in this view.
- This view was backfilled on January 22, 2022 to include dependencies prior to making the view available. Snowflake continues to record
  dependencies after this date.

  Note that if a view or [UDF](/developer-guide/udf/udf-overview) was invalid due to a missing dependency prior to this date and
  the missing dependency is fixed later, Snowflake does not record the dependency for the view or UDF.

  For example, if you created a view that depends on a table on December 1, 2021, dropped the table on the same day, and then undropped the
  table on February 1, 2022, Snowflake does not record that the view depends on the table.

  As a workaround, create or replace the view or UDF to so that this view records the dependency.

# Data sharing usage notes

General notes:
:   The view updates assume the share is not deleted.

    The view schema (i.e. column names, data types, and values) remains the same with these exceptions:

    - The value for the REFERENCED\_OBJECT\_ID column in the consumer account is always NULL for a shared object.

      This value prevents a customer from discovering the source object in the provider account.
    - The value for REFERENCED\_OBJECT\_DOMAIN is `TABLE` for all table-like objects.

Snowflake objects:
:   Shared objects, such as Account Usage views, are now supported as referenced objects.

    For example, if a user-defined view depends on data from another Account Usage view, such as LOGIN\_HISTORY, the OBJECT\_DEPENDENCIES view
    in the consumer account specifies the LOGIN\_HISTORY view as the referenced object.

Rename notes:
:   When a provider renames a shared database, shared schema, or shared object:

    - The consumer OBJECT\_DEPENDENCIES view record shows the record of the original name for the database, schema, or object prior to
      the renaming, not the renamed object.

      Newly renamed shared objects are not shown in the consumer OBJECT\_DEPENDENCIES view to prevent the consumer from determining the object
      lifecycle in the provider account. A new referencing object would need to refer to the newly renamed object in order for the renamed
      object to appear in the local OBJECT\_DEPENDENCIES view in the consumer account.
    - Renaming the shared database preserves the dependency in the consumer account.
    - Renaming a shared schema or shared objects in a shared schema breaks the dependency in the consumer account.

    If the consumer renames a shared database, all existing dependencies on that database break. Consequently, Snowflake removes the
    corresponding records from the OBJECT\_DEPENDENCIES view in the consumer account.

    For example, the shared database contains a view named `db1_shared.views.view_1_shared`. The consumer renames the shared database to
    `mydb`. The view now has a fully-qualified name of `mydb.views.view_1_shared`. Snowflake removes the row specifying
    `db1_shared.views.view_1_shared` in the consumer’s OBJECT\_DEPENDENCIES view because the dependency on the database named
    `db1_shared` is broken.

Not supported:
:   The `BY_ID` dependency type for referenced objects is not supported.

    - [Limitations](/user-guide/object-dependencies#label-object-dependencies-limitations)
    - [Object dependencies with snowflake features and services](/user-guide/object-dependencies#label-object-dependencies-features)
