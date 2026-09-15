# REPLICATION\_DATABASES view

This Information Schema view displays a row for each primary and secondary database (i.e. database for which replication has been enabled) in your organization.

Note

This view uses Snowflake terminology of “database”, whereas other Information Schema views use the standard INFORMATION\_SCHEMA terminology of “catalog”. The two terms have the same meaning.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| REGION\_GROUP | VARCHAR | [Region group](/user-guide/admin-account-identifier#label-region-groups) where the account that stores the database is located. |
| SNOWFLAKE\_REGION | VARCHAR | Snowflake Region where the account that stores the database is located. A Snowflake Region is a distinct location within a cloud platform region that is isolated from other Snowflake Regions. A Snowflake Region can be either multi-tenant or single-tenant (for a Virtual Private Snowflake account). |
| ACCOUNT\_NAME | VARCHAR | Name of the account in which the database is stored. |
| DATABASE\_NAME | VARCHAR | Name of the database. |
| COMMENT | VARCHAR | Comment for the database. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the database was created. |
| IS\_PRIMARY | VARCHAR | Whether the database is a primary database; otherwise, is a secondary database. |
| PRIMARY | VARCHAR | Name of the primary database. |
| REPLICATION\_ALLOWED\_TO\_ACCOUNTS | VARCHAR | Where `IS_PRIMARY` is TRUE, shows the fully-qualified names of accounts where replication has been enabled for this primary database. |
| FAILOVER\_ALLOWED\_TO\_ACCOUNTS | VARCHAR | Where `IS_PRIMARY` is TRUE, shows the fully-qualified names of accounts where failover has been enabled for this primary database. |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges. The view does not honor the MANAGE GRANTS privilege and consequently may show less
  information compared to a SHOW command when both are executed by a user who holds the MANAGE GRANTS privilege.
