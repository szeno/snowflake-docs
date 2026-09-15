# Auto-fulfillment objects

Before continuing, be sure that you understand the objects that are supported for Cross-Cloud Auto-Fulfillment (auto-fulfillment), how objects may depend on account roles, the internal objects that Snowflake creates for auto-fulfillment, and what exactly gets fulfilled by object-level auto-fulfillment.

## Objects supported for auto-fulfillment

The database objects included in *or referenced by* your
listing must contain only objects supported for auto-fulfillment.

Depending on your data product, different objects are supported:

| Object | Share (Database) | Application package |
| --- | --- | --- |
| Table | ✔ | ✔ |
| Open table (Apache Iceberg™, Delta Lake) | ✔ | ✔ |
| View (Regular, aka Non-Secure) | ✔ | ✔ |
| View (Materialized) | ✔ | ✔ |
| View (Secure) | ✔ | ✔ |
| View (Semantic) | ✔ | ✔ |
| Secure view that references data stored in other databases using the REFERENCE\_USAGE privilege. | ✔ | ✔ |
| Secure view that references a directory table of an internal stage (not external). For more information, see [Share unstructured data with a secure view](/user-guide/unstructured-data-sharing). | ✔ | ✔ |
| Cortex Knowledge Extensions (CKEs) | ✔ |  |
| Cortex Agents | ✔ |  |
| Dynamic Table | ✔ | ✔ (only from the application package) |
| Database Roles | ✔ | ✔ |
| SQL UDF/UDTF (Regular, also known as non-secure) | ✔ | ✔ (when called from shared views in referenced databases) |
| SQL UDF/UDTF (Secure) | ✔ | ✔ (when called from shared views in referenced databases) |
| Stored Procedure (not used by sharing) | ✔ | ✔ |
| Masking and Row Access Policies | ✔ | ✔ |
| Tags | ✔ | ✔ |
| Policies | ✔ | ✔ |
| Tasks (not used by sharing) | ✔ | ✔ |
| Alerts (not used by sharing) | ✔ | ✔ |
| Secrets (not used by sharing) | ✔ | ✔ |

Expand

Show lessSee more

If an object on this list is designated as part of a replication or failover group, then it’s not supported for auto-fulfillment.
See [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro) for details. If a primary database contains a hybrid table, the refresh operation fails.
For details, see the [Snowflake Community forum](https://community.snowflake.com/s/article/Auto-fulfillment-error-SQL-execution-error-Primary-database-contains-an-entity-of-type-Table-Replication-of-a-database-with-this-entity-type-is-not-supported).

If your data product contains or references objects other than the listed supported objects, you must update your data product.

## Auto-fulfillment for objects that depend on account roles

Auto-fulfillment does not replicate account roles. Instead, objects in SSAs are owned by the ACCOUNTADMIN role.

If your share or application package contains objects that depend on an account role, the object might work differently than you
expect when shared with consumers. For example:

- If you share a secure view that includes data protected by a policy using the [INVOKER\_ROLE](/sql-reference/functions/invoker_role) context function, the policy
  might evaluate to a different value than in the provider account region because the view owner role is different.
- If you share a secure view where the objects referenced by the view are restricted to an account role, such as a table where
  only the SECURITYADMIN role has SELECT privileges, the view might fail to expand when queried by a user without the SECURITYADMIN role
  in the provider account, but return results when queried by a user without the SECURITYADMIN role in the consumer account.

Instead of using account roles, use database roles. For more information, see [Share data protected by a policy](/user-guide/data-sharing-policy-protected-data)
and [IS\_DATABASE\_ROLE\_IN\_SESSION](/sql-reference/functions/is_database_role_in_session).

Snowflake Marketplace calculates compute costs for listing auto-fulfillment to VPS regions by using VPS rates. For details on VPS rates, see [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Internal Snowflake objects created for auto-fulfillment

Snowflake creates the following internal objects to support Cross-Cloud Auto-Fulfillment:

| Object Type | Name |
| --- | --- |
| Roles | SNOWFLAKE$GDS\_RL  AUTO\_FULFILLMENT\_EXECUTOR |
| Database | SNOWFLAKE$GDS |
| Replication groups | Prefixed with `SNOWFLAKE$GDS` |

Expand

Show lessSee more

These internal objects are used to perform tasks for auto-fulfillment, such as to create a secure share area in another region, and
create a database to store objects used for auto-fulfillment, such as fulfillment tasks.

These internal objects appear when you run [SHOW DATABASES](/sql-reference/sql/show-databases), [SHOW ROLES](/sql-reference/sql/show-roles), or [SHOW REPLICATION GROUPS](/sql-reference/sql/show-replication-groups) respectively.
Do not modify these objects or grant them to other users or roles.

### Object-level auto-fulfillment

When you configure object-level auto-fulfillment, SUB\_DATABASE is used for supported objects. Objects that are referenced by these
objects must also be supported. For a list of supported objects,
refer to the [Objects supported for auto-fulfillment](#label-listings-auto-fulfill-supported-objects) topic on this page.

![Diagram showing a auto-fulfillment of a listing to additional regions and clouds.](/static/images/ds-diagram-object-level-replication.png)

1. The first consumer in a region gets the listing.
2. Auto-fulfillment transfers the objects in the share to the secure share area.
3. Any consumer that gets the listing gets the data product from the secure share area in their Snowflake region.

## What gets fulfilled by object-level auto-fulfillment

When you use SUB\_DATABASE (object-level) auto-fulfillment for your data product, only the objects granted directly to the share or
app, or referenced by an object in your share or app, are auto-fulfilled.

For example:

| Object in data product | What is transferred |
| --- | --- |
| Table in a database and schema | Table |
| Secure view created from a table in the same database | Secure view and table |
| (Deprecated) Table in a database using FULL\_DATABASE auto-fulfillment | Entire database |
| Table in a database using SUB\_DATABASE auto-fulfillment | Table |
| Application package using SUB\_DATABASE\_WITH\_REFERENCE\_USAGE auto-fulfillment | The application package |

Expand

Show lessSee more
