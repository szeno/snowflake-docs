Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage)

# CONTACTS view

This Account Usage view displays a row for each [contact](/user-guide/contacts-using) in the account.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| CONTACT\_ID | NUMBER | Internal/system-generated identifier of the contact. |
| CONTACT\_NAME | VARCHAR | Name of the contact. |
| CONTACT\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier of the schema in which the contact exists. |
| CONTACT\_SCHEMA | VARCHAR | Name of the schema in which the contact exists. |
| CONTACT\_DATABASE\_ID | NUMBER | Internal/system-generated identifier of the database in which the contact exists. |
| CONTACT\_DATABASE | VARCHAR | Name of the database in which the contact exists. |
| CONTACT\_OWNER | VARCHAR | Name of the role that owns the contact. |
| CONTACT\_OWNER\_ROLE\_TYPE | VARCHAR | Type of role that owns the object. Either ROLE, DATABASE\_ROLE, or APPLICATION (if a Snowflake Native App owns the object).  Deleted contacts have a NULL value. |
| CONTACT\_USERS | ARRAY | Array of Snowflake users to contact. |
| CONTACT\_EMAIL\_DISTRIBUTION\_LIST | VARCHAR | Email address used to communicate with the contact. |
| CONTACT\_URL | VARCHAR | URL used to communicate with the contact. |
| COMMENT | VARCHAR | Comments for the contact, if any. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the contact was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the contact was dropped or the date and time when its parent was dropped. |

Expand

Show lessSee more

## Usage notes

- Latency for the view is 2 hours.
