Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# ROLES view

This Account Usage view can be used to query a list of all roles defined in the account. The data is retained for 365 days (1 year).

## Columns

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

- Latency for the view may be up to 120 minutes (2 hours).

- The view does not include database roles for databases created from shares.

# Internal Snowflake role for Snowsight

The first time [Snowsight](/user-guide/ui-snowsight) is accessed in an account, Snowflake creates the internal APPADMIN and
WORKSHEETS\_APP\_RL roles to support the web interface. These roles are used to cache query results in an internal stage in your account.
This cached data is encrypted and protected by the key hierarchy for the account. The limited privileges granted to these internal roles
only allow Snowsight to access the internal stage to store those results. Thes roles cannot list objects in your account or access
data in your tables. For more information, see [Getting started with Snowsight](/user-guide/ui-snowsight-gs).
