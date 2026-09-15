# USAGE\_PRIVILEGES view

In accordance with the ANSI standard, this view displays a row for each privilege defined for sequences in the specified (or current) database.

To view privileges on other types of objects, use the [OBJECT\_PRIVILEGES view](/sql-reference/info-schema/object_privileges) view.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| GRANTOR | VARCHAR | Role who granted the usage privilege |
| GRANTEE | VARCHAR | Role to whom the usage privilege is granted |
| GRANTED\_TO | VARCHAR | Type of object that has been granted the privilege |
| OBJECT\_CATALOG | VARCHAR | Database containing the object on which the privilege is granted |
| OBJECT\_SCHEMA | VARCHAR | Schema containing the object on which the privilege is granted |
| OBJECT\_NAME | VARCHAR | Name of the object on which the privilege is granted |
| OBJECT\_TYPE | VARCHAR | Type of the object on which the privilege is granted |
| PRIVILEGE\_TYPE | VARCHAR | Type of the granted privilege |
| IS\_GRANTABLE | VARCHAR | Whether the privilege was granted WITH GRANT OPTION |
| CREATED | TIMESTAMP\_LTZ | Creation time of the privilege |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges.
