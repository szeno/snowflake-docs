Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# ROLES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to query a list of all roles defined in each account.

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ROLE\_ID | NUMBER | Internal/system-generated identifier for the role. |
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time (in the UTC time zone) when the role was created. |
| DELETED\_ON | TIMESTAMP\_LTZ | Date and time (in the UTC time zone) when the role was deleted. |
| NAME | VARCHAR | Name of the role. |
| COMMENT | VARCHAR | Comment for the role. |
| OWNER | VARCHAR | Role with the OWNERSHIP privilege on the object. |
| ROLE\_TYPE | VARCHAR | Either `ROLE`, `DATABASE_ROLE`, `INSTANCE_ROLE`, or `APPLICATION_ROLE`. |
| ROLE\_DATABASE\_NAME | VARCHAR | Name of the database that contains the database role if the role is a database role. |
| ROLE\_INSTANCE\_ID | NUMBER | Internal/system-generated identifier for the class instance that the role belongs to. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| IS\_FROM\_ORGANIZATION\_USER\_GROUP | BOOLEAN | If TRUE, the role was imported from an [organization user group](/user-guide/organization-users#label-org-users-groups). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The view does not include database roles for databases created from shares.

# Internal Snowflake role for Snowsight

The first time [Snowsight](/user-guide/ui-snowsight) is accessed in an account, Snowflake creates the internal APPADMIN and
WORKSHEETS\_APP\_RL roles to support the web interface. These roles are used to cache query results in an internal stage in your account.
This cached data is encrypted and protected by the key hierarchy for the account. The limited privileges granted to these internal roles
only allow Snowsight to access the internal stage to store those results. Thes roles cannot list objects in your account or access
data in your tables. For more information, see [Getting started with Snowsight](/user-guide/ui-snowsight-gs).
